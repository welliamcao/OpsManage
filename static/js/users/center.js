function makeRandomId() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (var i = 0; i < 8; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  return text;
}
var webssh = false
function make_terminal(element, size, ws_url) { 
    var term = new Terminal({
        cols: size.cols,
        rows: size.rows,
        screenKeys: true,
        useStyle: true,
        cursorBlink: true,  // Blink the terminal's cursor
    });         	
    if (webssh) {
        return;
    }        
    webssh = true;        	
    term.open(element, false);
    term.write('正在连接...')
/*             term.fit(); */
    var ws = new WebSocket(ws_url);
    ws.onopen = function (event) {
        term.resize(term.cols, term.rows);
/*                 ws.send(JSON.stringify(["id", id,term.cols, term.rows]));  */
        term.on('data', function (data) {
            <!--console.log(data);-->
             ws.send(data); 
        });

        term.on('title', function (title) {
            document.title = title;
        });
        ws.onmessage = function (event) {
        	term.write(event.data);
        };      
    };
    ws.onerror = function (e) {
    	term.write('\r\n连接失败')
    	ws = false
    };
/*    ws.onclose = function () {
        term.destroy();
    }; */     
    return {socket: ws, term: term};
}

var selectState = false;  
function checkAllBox(){ 
  	var qcheck=document.getElementsByName("ckbox");
  	for (var i = 0; i < qcheck.length; i++)  
	  {  
	    var checkbox = qcheck[i];  
	    checkbox.checked = !selectState; 
	  }  
  	selectState = !selectState; 
} 

function format (dataList) {
    var trHtml = '';
	for (var i=0; i <dataList["astList"].length; i++){	
	    trHtml += '<tr><td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["astList"][i]["name"] +':</td>'+ '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["astList"][i]["value"] +'</td></tr>'	    
	};	
	var nktTrHtml = '';
    if (dataList["nktList"].length){
    	var nktTdHtml = '';
		for (var i=0; i <dataList["nktList"].length; i++){	
			if ( dataList["nktList"][i]["status"]=="1"){
				var status = '<span class="label label-success">on</span>' 
			}else{
				var status = '<span class="label label-danger">off</span>'
			}
			nktTdHtml += '</tr>' + 
						 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["name"] +'</td>'+ 
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["mac"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["ipv4"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["speed"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["mtu"] +'</td>' +
					   	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ status +'</td>' +
					   	 '</tr>'
		};	   
		nktTrHtml += nktTrHtml + nktTdHtml 
    }
	var nHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    			'<legend>网卡信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				'<tr>' +
	    					'<th>Name</th>' +
	    					'<th>MAC</th>' +
	    					'<th>IPV4</th>' +
	    					'<th>Speed</th>' +
	    					'<th>MTU</th>' +
	    					'<th>Status</th>' +
	    				'</tr>' + nktTrHtml  +
	    				'</table>'
				'</div>'; 	
		
	    var vHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    			'<legend>硬件信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				 trHtml  +
	    				'</table>'
				'</div>'; 				
    return '<div class="row">'+ vHtml + '</div>' + nHtml + '</div>';
}	


function RefreshAssetsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList )
	{
	  table = $('#'+tableId).dataTable();
	  oSettings = table.fnSettings();
	  
	  table.fnClearTable(this);
	
	  for (var i=0; i<dataList.length; i++)
	  {
	    table.oApi._fnAddData(oSettings, dataList[i]);
	  }
	
	  oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	  table.fnDraw();	  
	});
}

function RefreshChoiceAssets(){
	var btnObj = $(this);
	btnObj.attr('disabled',true);
	var serverId = [];
	var ips = ''
    $.each($('input[type=checkbox]input[name="ckbox"]:checked'),function(){
    	ips += '<strong><code>' + $(this).parent().parent().find("td").eq(5).text() + '</code></strong>&nbsp;'
    	serverId.push($(this).val())
    }); 
  	if (serverId.length > 0){
	    $.confirm({
	        type: 'blue',
	        title: '更新资产',
	        content: '确认更新这些资产:<br>' + ips,
	        buttons: {
	            '更新': {
	                btnClass: 'btn-blue',
	                action: function() {
						$.ajax({
							  type: 'POST',
							  url: '/assets/batch/',
							  dataType:"json",
							  data:{
								  'ids':serverId,
								  'model':'batch'
							  },
							  success:function(response){	
								var sip = '';
								var fip = '';
								var modal = '';
								for  (var i = 0; i < response['data']['success'].length; i++){
									 sip += response['data']['success'][i] + '<br>'
								}
								for  (var i = 0; i < response['data']['failed'].length; i++){
									 fip += response['data']['failed'][i] + '<br>'
								}	
								msg = '成功：'+ '<br>' + sip + '<br>' + '失败：'+ '<br>' + fip;	
								if (response['code']==200){
									new PNotify({
										title: 'Success!',
										text: msg,
										type: 'success',
										styling: 'bootstrap3',
										delay: 18000
									}); 
									RefreshAssetsTable("assetsListTable","/api/assets/")
								}
								else{
									new PNotify({
										title: 'Ops Failed!',
										text: response["msg"],
										type: 'error',
										styling: 'bootstrap3',
										delay: 18000
									}); 
								}
								btnObj.removeAttr('disabled');		            
							  },
							  error:function(response){
								btnObj.removeAttr('disabled');
								new PNotify({
									title: 'Ops Failed!',
									text: '资产修改失败',
									type: 'error',
									styling: 'bootstrap3'
								}); 
							  }
							});
	                }
	            },
        	'取消': function() {},
	        }
	    }); 		
  	}
  	else{
		$.alert({
		    title: '批量更新资产',
		    content: '请至少选择一个资产!',
		    type: 'red',
		});	 
  		btnObj.removeAttr('disabled');
  	}	
}

function DeleteChoiceAssets(){
	var btnObj = $(this);
	btnObj.attr('disabled',true);
	var serverId = [];
	var ips = ''
    $.each($('input[type=checkbox]input[name="ckbox"]:checked'),function(){
    	ips += '<strong><code>' + $(this).parent().parent().find("td").eq(5).text() + '</code></strong>&nbsp;'
    	serverId.push($(this).val())
    });  
  	if (serverId.length > 0){
	    $.confirm({
	        type: 'red',
	        title: '删除资产',
	        content: '确认删除这些资产:<br>' + ips,
	        buttons: {
	            '删除': {
	                btnClass: 'btn-blue',
	                action: function() {
  		         		 $.ajax({
	   		      			  type: 'DELETE',
	   		      			  url: '/assets/batch/',
	   		      			  dataType:"json",
	   		      			  data:{
	   		      				  'assetsIds':serverId,
	   		      			  },
	   		      		      success:function(response){	
	   		      		    	var sip = '';
	   		      		    	var fip = '';
	   		      		    	var modal = '';
	   		      	    		for  (var i = 0; i < response['data']['success'].length; i++){
	   		      	    			 sip += response['data']['success'][i] + '<br>'
	   		      	    		}
	   		      	    		for  (var i = 0; i < response['data']['failed'].length; i++){
	   		      	    			 fip += response['data']['failed'][i] + '<br>'
	   		      	    		}	
	   		      	    		msg = '成功：'+ '<br>' + sip + '<br>' + '失败：'+ '<br>' + fip;	
	   		      			    	if (response['code']==200){
	   		      		            	new PNotify({
	   		      		                    title: 'Success!',
	   		      		                    text: msg,
	   		      		                    type: 'success',
	   		      		                    styling: 'bootstrap3',
	   		      		                    delay: 18000
	   		      		                }); 	
	   		      		    	}
	   		      		    	else{
	   		      	            	new PNotify({
	   		      	                    title: 'Ops Failed!',
	   		      	                    text: response["msg"],
	   		      	                    type: 'error',
	   		      	                    styling: 'bootstrap3',
	   		      	                    delay: 18000
	   		      	                }); 
	   		      		    	}
	   		      			    btnObj.removeAttr('disabled');		            
	   		      		      },
	   		                    error:function(response){
	   		                  	btnObj.removeAttr('disabled');
	   		                  	new PNotify({
	   		                          title: 'Ops Failed!',
	   		                          text: '资产修改失败',
	   		                          type: 'error',
	   		                          styling: 'bootstrap3'
	   		                      }); 
	   		                    }
	   		      			});	
	                }
	            },
        	'取消': function() {},
	        }
	    }); 		
  	}
  	else{
		$.alert({
		    title: '批量删除资产',
		    content: '请至少选择一个资产!',
		    type: 'red',
		});	 
  		btnObj.removeAttr('disabled');
  	}
};

$(document).ready(function() {
	
	if($("#assetsListTable").length){
	    var buttons = [
		                {
		                	text: '<span class="fa fa fa-download"></span>',
		                    extend: "csv",
		                    className: "btn-sm"
		                },	
		                {
		                	text: '<span class="fa fa fa-print"></span>',
		                    extend: "print",
			                className: "btn-sm"
			            },	
					    {
					        text: '<span class="fa fa-cloud-upload"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	$("#AssetsImportModal").modal('show');
					        }
					    },	
					    {
					        text: '<span class="fa fa-refresh"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	RefreshChoiceAssets()
					        }
					    },		
					    {
					        text: '<span class="fa fa-trash-o"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	DeleteChoiceAssets()
					        }
					    },						    
	    ] 		
		
	    var columns = [
	                   	{
	                       "className":      'details-control',
	                       "orderable":      false,
	                       "data":           null,
	                       "defaultContent": ''
	                   	},
	                   	{
	                       "orderable":      false,
	                       "data":           null,
	                       "defaultContent": ''
	                   	},
	                    {"data": "id"},
		                {"data": "detail.ip"},
		                {
		                	"data": "detail.system",
		                	"defaultContent": "无数据"
		                },	
		                {
		                	"data": "detail.kernel",
		                	"defaultContent": "无数据"
		                },	
		                {
		                	"data": "detail.cpu_number",
		                	"defaultContent": "无数据"
		                },
		                {
		                	"data": "detail.ram_total",
		                	"defaultContent": "无数据"
		                },
		                {
		                	"data": "detail.disk_total",
		                	"defaultContent": "无数据"
		                },	
		                {
		                	"data": "put_zone",
		                	"defaultContent": "无数据"
		                },
		               ]	    
	    
	    var columnDefs = [	
							{
								targets: [1],
								render: function(data, type, row, meta) {
									return '<input type="checkbox" class="flat" value="'+row.id+'" name="ckbox"/></td>'
								},
							},							
  	    		        {
	    	    				targets: [10],
	    	    				render: function(data, type, row, meta) {	
	    	                        if(row.assets_type == 'server'){
			                            var hw = '<button type="button" name="btn-assets-hw" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align"><span class="fa fa-hdd-o" aria-hidden="true"></span></button>'		    	               
	    	                        }else{
	    	                        	var hw = '<button type="button" name="btn-assets-hw" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align" disabled><span class="fa fa-hdd-o" aria-hidden="true"></span></button>'		    	   
	    	                        }
	    	                        return '<div class="btn-group btn-group-sm">' +
				                            '<button type="button" name="btn-assets-alter" value="'+ row.id +'" class="btn btn-default" aria-label="Center Align"><a href="/assets/manage/?id='+ row.id +'&model=edit" target="view_window"><span class="glyphicon glyphicon-check" aria-hidden="true"></span></a>' +
				                            '</button>'+ 
				                            '<button type="button" name="btn-assets-info" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align" data-toggle="modal" data-target=".bs-example-modal-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>' +
				                            '</button>'+ 	                            
				                            '<button type="button" name="btn-assets-update" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align"><span class="glyphicon glyphicon-refresh" aria-hidden="true"></span>' +
				                            '</button>'+ hw +      
				                            '<button type="button" name="btn-assets-webssh" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-desktop" aria-hidden="true"></span>' +
				                            '</button>'+ 				                            
				                            '<button type="button" name="btn-assets-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +
				                            '</button>'+ 
				                          '</div>'; 	    	                        
	    	    				},
	    	    				"className": "text-center",
  	    		        },
  	    		      ]	    
	    
		var assetsTable = $('#assetsListTable').DataTable({
		    "dom": "Bfrtip",
		    "buttons":buttons,
    		"bScrollCollapse": false, 				
    	    "bRetrieve": true,			
    		"destroy": true, 
    		"data":	requests("get","/api/assets/"),
    		"columns": columns,
    		"columnDefs" :columnDefs,			  
    		"language" : language,
    		"order": [[ 0, "ase" ]],
    		"autoWidth": false	    			
		});		
		
	    $('#assetsListTable tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = assetsTable.row( tr );	        
	        aId = row.data()["id"];
	        $.ajax({
	            url : "/api/assets/info/"+aId+"/",
	            type : "post",
	            async : false,
	            data : {"id":aId},
	            dataType : "json",
	            success : function(result) {
	            	dataList = result.data;
	            }
	        });	        
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( format(dataList) ).show();
	            tr.addClass('shown');
	        }
	    });			
		
	}
	
    $('#assetsListTable tbody').on('click','button[name="btn-assets-delete"]',function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var ip = td.eq(5).text();  
		$.confirm({
		    title: '删除确认',
		    content: "确认删除【<strong>"+ip+"</strong>】?",
		    type: 'red',
		    buttons: {
		        删除: function () {
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/assets/" + vIds + '/',  
				            error: function(request) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: "删除失败",
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });       
				            },  
				            success: function(request) {  
				            	new PNotify({
				                    title: 'Success!',
				                    text: "删除成功",
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshAssetsTable("assetsListTable","/api/assets/")
				            }  
				    	});
		        },
		         取消: function () {
		            return true;			            
		        },			        
		    }
		});	  	
    });	
	
	//更新资产
	$('#assetsListTable tbody').on('click','button[name="btn-assets-update"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var ip = td.eq(5).text(); 
		$.confirm({
		    title: '更新确认',
		    content: ip,
		    type: 'blue',
		    buttons: {
		              更新: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:"/assets/modf/" + vIds + '/', 
			            data:{"model":'setup',"ids":vIds},
			            error: function(request) {  
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: "更新失败",
			                    type: 'error',
			                    styling: 'bootstrap3'
			                });       
			            },  
			            success: function(request) {  
			            	if (request["code"] == "200"){
				            	new PNotify({
				                    title: 'Success!',
				                    text: request["msg"],
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshAssetsTable("assetsListTable","/api/assets/")			            		
			            	}else{
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: request["msg"],
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });  				            		
			            	}

			            }  
			    	});
		        },
			        取消: function () {
			            return true;			            
			        },			        
			    }
		});			
		$(this).attr('disabled',false);
	});    
    
	$('#assetsListTable tbody').on('click','button[name="btn-assets-info"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var ip = td.eq(5).text();     	
    	$.ajax({  
            cache: true,  
            type: "GET",  
            url:"/assets/manage/?id="+ vIds +"&model=info",  
            async: false,  
            error: function(response) {  
            	console.log(response)
            },  
            success: function(response) {   	
            	if (Object.keys(response["data"]).length > 0){
            		switch (response["data"]["status"])
            		{
	            		case 0:
	            		  status = '<span class="label label-success">已上线</span>';
	            		  break;
	            		case 1:
	            		  status = '<span class="label label-warning">已下线</span>';
	            		  break;
	            		case 2:
	            		  status = '<span class="label label-default">维修中</span>';
	            		  break;
	            		case 3:
	            		  status = '<span class="label label-info">已入库</span>';
	            		  break;
	            		case 4:
	            		  status = '<span class="label label-primary">未使用</span>';
	            		  break;
            		}
            		switch (response["data"]["assets_type"])
            		{
	            		case 'server':
	            			assets_type = '<strong>物理服务器</strong>';
	            		  	break;
	            		case 'vmser':
	            			assets_type = '<strong>虚拟机</strong>';
	            			break;
	            		case 'switch':
	            			assets_type = '<strong>交换机</strong>';
	            			break;
	            		case 'route':
	            			assets_type = '<strong>路由器</strong>';
	            			break;
	            		case 'firewall':
	            			assets_type = '<strong>防火墙</strong>';
	            			break;
	            		case 'storage':
	            			assets_type = '<strong>存储设备</strong>';
	            			break;	
	            		case 'printer':
	            			assets_type = '<strong>打印机</strong>';
			            	break;	
	            		case 'scanner':
	            			assets_type = '<strong>扫描仪</strong>';
			            	break;	
	            		case 'wifi':
	            			assets_type = '<strong>WIFI设备</strong>';
			            	break;				            	
            		}             		
            		var ulTag = '<ul class="list-unstyled timeline" id="assets_info">';
            		var serverLiTags = '';
            		var netcardLiTags = '';
            		var ramLiTags = '';
            		var diskLiTags = '';            		
            		var baseLiTags  =  '<li>' +
										  '<div class="block">' +
											'<div class="tags">' +
											  '<a href="" class="tag">' +
												'<span>基础信息</span>' +
											  '</a>' +
											'</div>' +
											'<div class="block_content">' +
							                    '<table class="table table-striped">' +		                
							                      '<tbody>' +
							                        '<tr>' +
							                          '<td>资产类型 :</td>' +
							                         ' <td>'+ assets_type +'</td>' +
							                          '<td> 资产编号  :</td>' +
							                          '<td>'+ response["data"]["name"] +'</td>' +			                         
							                        '</tr>' +
							                        '<tr>' +
							                          '<td>设备序列号 :</td>' +
							                          '<td>'+ response["data"]["sn"] +'</td>' +
							                          '<td>购买日期 : </td>' +
							                          '<td>'+ response["data"]["buy_time"] +'</td>' +			                          
							                        '</tr>' +		
							                        '<tr>' +
							                          '<td>过保日期 :</td>' +
							                          '<td>'+ response["data"]["expire_date"] +'</td>' +
							                          '<td>管理IP:</td>' +
							                          '<td>'+ response["data"]["management_ip"] +'</td>' +			                          
							                        '</tr>' +
							                        '<tr>' +
							                          '<td>购买人 : </td>' +
							                          '<td>'+ response["data"]["buy_user"] +'</td>' +
							                          '<td>生产制造商  :</td>' +
							                          '<td>'+ response["data"]["manufacturer"] +'</td>' +			                          
							                        '</tr>' +		
							                        '<tr>' +
							                          '<td>设备型号 :</td>' +
							                          '<td>'+ response["data"]["model"] +'</td>' +
							                          '<td>供货商 : </td>' +
							                          '<td>'+ response["data"]["provider"] +'</td>' +			                          
							                        '</tr>' +	
							                        '<tr>' +
							                          '<td>放置区域 :</td>' +
							                          '<td>'+ response["data"]["put_zone"] +'</td>' +
							                          '<td>机柜信息 : </td>' +
							                          '<td>'+ response["data"]["cabinet"] +'</td>' +			                          
							                        '</tr>' +	
							                        '<tr>' +
							                          '<td>设备状态 : </td>' +
							                          '<td>'+ status +'</td>' +
							                          '<td>使用组 :</td>' +
							                          '<td>'+ response["data"]["group"] +'</td>' +			                          
							                        '</tr>' +
							                        '<tr>' +
							                          '<td>所属项目 : </td>' +
							                          '<td>'+ response["data"]["project"] +'</td>' +
							                          '<td>所属应用 : </td>' +
							                          '<td>'+ response["data"]["service"] +'</td>' +			                          
							                        '</tr>' +			                        
							                      '</tbody>' +
							                    '</table>' +							
											'</div>' +
										  '</div>' +
										'</li>';
            		if (Object.keys(response["data"]["server"]).length > 0){
                		serverLiTags = '<li>' +
						  '<div class="block">' +
							'<div class="tags">' +
							  '<a href="" class="tag">' +
								'<span>硬件信息</span>' +
							  '</a>' +
							'</div>' +
							'<div class="block_content">' +
			                    '<table class="table table-striped">' +		                
			                      '<tbody>' +
			                        '<tr>' +
			                          '<td>主机名 :</td>' +
			                         ' <td>'+ response["data"]["server"]["hostname"] +'</td>' +
			                          '<td>操作系统:</td>' +
			                          '<td>'+ response["data"]["server"]["system"]+'</td>' +			                         
			                        '</tr>' +
			                        '<tr>' +
			                          '<td>内核版本 :</td>' +
			                          '<td>'+ response["data"]["server"]["kernel"] +'</td>' +
			                          '<td>IP地址 : </td>' +
			                          '<td>'+ response["data"]["server"]["ip"] +'</td>' +			                          
			                        '</tr>' +		
			                        '<tr>' +
			                          '<td>CPU :</td>' +
			                          '<td>'+ response["data"]["server"]["cpu"] +'</td>' +
			                          '<td>CPU个数:</td>' +
			                          '<td>'+ response["data"]["server"]["vcpu_number"] +'</td>' +			                          
			                        '</tr>' +
			                        '<tr>' +
			                          '<td>硬盘大小(GB) : </td>' +
			                          '<td>'+ response["data"]["server"]["disk_total"] +'</td>' +
			                          '<td>Raid类型:</td>' +
			                          '<td>'+ response["data"]["server"]["raid"] +'</td>' +			                          
			                        '</tr>' +		
			                        '<tr>' +
			                          '<td>出口线路 :</td>' +
			                          '<td>'+ response["data"]["server"]["line"] +'</td>' +
			                          '<td>内存容量 (GB): </td>' +
			                          '<td>'+ response["data"]["server"]["ram_total"] +'</td>' +			                          
			                        '</tr>' +	
			                        '<tr>' +
			                          '<td>Swap容量:</td>' +
			                          '<td>'+ response["data"]["server"]["swap"] +'</td>' +
			                          '<td>Selinux : </td>' +
			                          '<td>'+ response["data"]["server"]["selinux"] +'</td>' +			                          
			                        '</tr>' +				                        
			                      '</tbody>' +
			                    '</table>' +							
							'</div>' +
						  '</div>' +
						'</li>';            			
            		}
            		if (Object.keys(response["data"]["networkcard"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["data"]["networkcard"].length; i++){
		                      if (response["data"]["networkcard"][i]["active"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["data"]["networkcard"][i]["device"] +'</td>' +
					                          '<td>'+ response["data"]["networkcard"][i]["macaddress"]+'</td>' +	
						                      '<td>'+ response["data"]["networkcard"][i]["ip"] +'</td>' +
						                      '<td>'+ response["data"]["networkcard"][i]["module"]+'</td>' +			
						                      '<td>'+ response["data"]["networkcard"][i]["mtu"]+'</td>' +
						                       status +
					                        '</tr>';
						};              			
            			netcardLiTags = '<li>' +
						  '<div class="block">' +
							'<div class="tags">' +
							  '<a href="" class="tag">' +
								'<span>网卡信息</span>' +
							  '</a>' +
							'</div>' +
							'<div class="block_content">' +
			                    '<table class="table table-striped">' +		                
			                      '<tbody>' +
			                        '<tr>' +
			                          '<td>Name</td>' +
			                          '<td>MAC</td>' +	
				                      '<td>IPV4</td>' +
				                      '<td>Speed</td>' +			
				                      '<td>MTU</td>' +				
				                      '<td>Status</td>' +			                        	
			                        '</tr>' + trTags +		                        
			                      '</tbody>' +
			                    '</table>' +							
							'</div>' +
						  '</div>' +
						'</li>';               			
						
            		}
            		if (Object.keys(response["data"]["ram"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["data"]["ram"].length; i++){
		                      if (response["data"]["ram"][i]["device_status"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["data"]["ram"][i]["device_model"] +'</td>' +
					                          '<td>'+ response["data"]["ram"][i]["device_volume"]+'</td>' +	
						                      '<td>'+ response["data"]["ram"][i]["device_brand"] +'</td>' +
						                      '<td>'+ response["data"]["ram"][i]["device_slot"]+'</td>' +			
						                       status +
					                        '</tr>';
						};              			
            			ramLiTags = '<li>' +
									  '<div class="block">' +
										'<div class="tags">' +
										  '<a href="" class="tag">' +
											'<span>内存明细</span>' +
										  '</a>' +
										'</div>' +
										'<div class="block_content">' +
						                    '<table class="table table-striped">' +		                
						                      '<tbody>' +
						                        '<tr>' +
						                          '<td>内存型号</td>' +
						                          '<td>内存容量(GB)</td>' +	
							                      '<td>生产商</td>' +
							                      '<td>Slot</td>' +					
							                      '<td>Status</td>' +			                        	
						                        '</tr>' + trTags +		                        
						                      '</tbody>' +
						                    '</table>' +							
										'</div>' +
									  '</div>' +
									'</li>';               			
						
            		}   
            		if (Object.keys(response["data"]["disk"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["data"]["disk"].length; i++){
		                      if (response["data"]["disk"][i]["device_status"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["data"]["disk"][i]["device_model"] +'</td>' +
					                          '<td>'+ response["data"]["disk"][i]["device_volume"]+'</td>' +	
					                          '<td>'+ response["data"]["disk"][i]["device_serial"] +'</td>' +
						                      '<td>'+ response["data"]["disk"][i]["device_brand"] +'</td>' +
						                      '<td>'+ response["data"]["disk"][i]["device_slot"]+'</td>' +			
						                       status +
					                        '</tr>';
						};              			
            			diskLiTags = '<li>' +
									  '<div class="block">' +
										'<div class="tags">' +
										  '<a href="" class="tag">' +
											'<span>硬盘明细</span>' +
										  '</a>' +
										'</div>' +
										'<div class="block_content">' +
						                    '<table class="table table-striped">' +		                
						                      '<tbody>' +
						                        '<tr>' +
						                          '<td>硬盘型号</td>' +
						                          '<td>硬盘容量</td>' +	
						                          '<td>序列号</td>' +	
							                      '<td>生产商</td>' +
							                      '<td>Slot</td>' +					
							                      '<td>Status</td>' +			                        	
						                        '</tr>' + trTags +		                        
						                      '</tbody>' +
						                    '</table>' +							
										'</div>' +
									  '</div>' +
									'</li>';               			
						
            		}            		
            		$("#assets_info").html(ulTag + baseLiTags + serverLiTags + netcardLiTags + ramLiTags + diskLiTags + '</ul>');	
            	}
            }  
    	});    	
		$(this).attr('disabled',false);
	});		
	
	$('#assetsListTable tbody').on('click','button[name="btn-assets-webssh"]',function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")	
		$("#myWebsshModalLabel").html('<p class="text-blank"><code><i class="fa fa fa-terminal"></i></code>'+td.eq(3).text()+'</p>')
		$("#websshConnect").val(vIds)	
		$('#webssh_tt').empty()
    	$('.bs-example-modal-webssh-info').modal({backdrop:"static",show:true}); 		
	})
	
    $("#websshConnect").on("click", function(){
    	var vIds = $(this).val();
    	var randromChat = makeRandomId()
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://' + window.location.host + '/ssh/' + vIds + '/' + randromChat + '/';
//        console.log(randromChat)
        websocket = make_terminal(document.getElementById('webssh_tt'), {rows: 30, cols: 140}, ws_path);  
        $(this).attr("disabled",true);
/*             $(".xterm-screen").css("width", "800px").css("height", "510px"); */
      });     
    
    $('.bs-example-modal-webssh-info').on('hidden.bs.modal', function () {
		try {
			websocket["socket"].close()
		}
		catch(err) {
			console.log(err)
		} 
		finally {
			webssh = false
		}    	
    	$("#websshConnect").attr("disabled",false);
    }); 	
	
	if($("#modf_user_pw_btn").length){
		$("#modf_user_pw_btn").on("click", function(){
	    	$.ajax({  
	            type: "POST",  
	            url:"/user/manage/",  
				data:{
					"type":"change_passwd",
					"id":$("#userid").val(),
	            	"password":$("#password").val(),
	            	"c_password":$("#c_password").val(),
	            },
	            error: function(response) {  
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });       
	            },  
	            success: function(response) {  
	            	if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: '修改成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 				            		
	            	}else{
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response["msg"],
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });  				            		
	            	}

	            }  
	    	});			
		})
	}	
})