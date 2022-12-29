function InitDataTableAssets(tableId,data,buttons,columns,columnDefs, page){
	oOverviewTable =$('#'+tableId).dataTable({
				    "dom": "Bfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data["results"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 20,
		            "select": {
		                "style":    'multi',
		                "selector": 'td:first-child'
		            },		    		
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
	});		
	  if (data['next']){
		  $("button[name='"+ page +"_page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='"+ page +"_page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='"+ page +"_page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='"+ page +"_page_previous']").attr("disabled", true).val();
	  }	  	  
}	

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

	function format (data) {
	    var astHtml = '';
	    if (data['assets_type'] == "物理机" || data['assets_type'] == "虚拟机"){
	    	astHtml = '<tr><td class="col-md-1 col-sm-12 col-xs-12">CPU型号:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['cpu'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">CPU个数:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['vcpu_number'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">硬盘容量:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['disk_total'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">内存容量:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['ram_total'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">操作系统:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['system'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">内核版本:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['kernel'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">主机名:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['hostname'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">资产备注:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['mark'] +'</td></tr>' 
	    }else{
	    	astHtml = '<tr><td class="col-md-1 col-sm-12 col-xs-12">CPU型号:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['cpu'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">内存容量:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['ram_total'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">背板带宽:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['bandwidth'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">端口总数:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['port_number'] +'</td></tr>' + 
	    			 '<tr><td class="col-md-1 col-sm-12 col-xs-12">资产备注:</td><td class="col-md-1 col-sm-12 col-xs-12">'+ data['detail']['mark'] +'</td></tr>'	    	
	    }
		var nktTrHtml = '';
	    if (data["networkcard"].length){
	    	var nktTdHtml = '';
			for (var i=0; i <data["networkcard"].length; i++){	
				if ( data["networkcard"][i]["active"]=="1"){
					var status = '<span class="label label-success">on</span>' 
				}else{
					var status = '<span class="label label-danger">off</span>'
				}
				nktTdHtml += '</tr>' + 
							 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device"] +'</td>'+ 
						  	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["macaddress"] +'</td>' +
						  	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["ip"] +'</td>' +
						  	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["module"] +'</td>' +
						  	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["mtu"] +'</td>' +
						   	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ status +'</td>' +
						   	 '</tr>'
			};	   
			nktTrHtml += nktTrHtml + nktTdHtml 
	    }
	    var businessTrHtml = ''
	    if (data["business"].length){
	    	var bussTdHtml = '';
			for (var i=0; i <data["business"].length; i++){	
				bussTdHtml += '</tr>' + 
							 	'<td class="col-md-1 col-sm-12 col-xs-12">关联业务线:</td>'+ 
						  	 	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["business"][i] +'</td>' +
						   	 '</tr>'
			};	   
			businessTrHtml += businessTrHtml + bussTdHtml 
	    }	    	    
	    var diskTrHtml = '';
	    if (data["disk"].length){
	    	var diskTdHtml = '';
			for (var i=0; i <data["disk"].length; i++){	
				if ( data["disk"][i]["active"]=="1"){
					var status = '<span class="label label-success">on</span>' 
				}else{
					var status = '<span class="label label-danger">off</span>'
				}
				diskTdHtml += '</tr>' + 
							 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device_volume"] +'</td>'+ 
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device_model"] +'</td>' +
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device_brand"] +'</td>' +
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device_serial"] +'</td>' +
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["networkcard"][i]["device_slot"] +'</td>' +
						   	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ status +'</td>' +
						   	 '</tr>'
			};	   
			diskTrHtml += diskTrHtml + diskTdHtml 
	    }	  
	    var ramTrHtml = '';
	    if (data["ram"].length){
	    	var ramTdHtml = '';
			for (var i=0; i <data["ram"].length; i++){	
				if ( data["ram"][i]["active"]=="1"){
					var status = '<span class="label label-success">on</span>' 
				}else{
					var status = '<span class="label label-danger">off</span>'
				}
				ramTdHtml += '</tr>' + 
							 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["ram"][i]["device_model"] +'</td>'+ 
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["ram"][i]["device_volume"] +'</td>' +
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["ram"][i]["device_brand"] +'</td>' +
						  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ data["ram"][i]["device_slot"] +'</td>' +
						   	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ status +'</td>' +
						   	 '</tr>'
			};	   
			ramTrHtml += ramTrHtml + ramTdHtml 
	    }		    
	    
		var netcardHtml = '<legend>网卡信息</legend>' +
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
			
 	    var astHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		    			'<legend>硬件信息</legend>' +
		    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
		    				 astHtml  +
		    				'</table>' +
					  '</div>'; 	
					
		var businessHtml = '<legend>业务线信息</legend>' +
			    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
									businessTrHtml +
			    				'</table>'								
		var diskHtml = '<legend>磁盘信息</legend>' +
		    					'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
		    						'<tr>' +
		    							'<th>硬盘容量</th>' +
		    							'<th>硬盘状态</th>' +
		    							'<th>硬盘型号</th>' +
		    							'<th>硬盘生产商</th>' +
		    							'<th>硬盘序列号</th>' +
		    							'<th>硬盘插槽</th>' +
		    						'</tr>' + diskTrHtml  +
		    					'</table>'	
		var ramHtml = '<legend>内存信息</legend>' +
		    					'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
		    						'<tr>' +
		    							'<th>内存型号</th>' +
		    							'<th>内存容量</th>' +
		    							'<th>内存生产商</th>' +
		    							'<th>内存插槽</th>' +
		    							'<th>内存状态</th>' +
		    						'</tr>' + ramTrHtml  +
		    					'</table>'			    						
	    return '<div class="col-md-6 col-sm-12 col-xs-12">'+ businessHtml + diskHtml + ramHtml + netcardHtml + '</div>' + astHtml;
	}


function RefreshAssetsTable(tableId, urlData, page){
	$.getJSON(urlData, null, function( dataList )
	{
	  table = $('#'+tableId).dataTable();
	  oSettings = table.fnSettings();
	  
	  table.fnClearTable(this);
	
	  for (var i=0; i<dataList["results"].length; i++)
	  {
	    table.oApi._fnAddData(oSettings, dataList["results"][i]);
	  }
	
	  oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	  table.fnDraw();	  
	  if (dataList['next']){
	   	  $("button[name='"+ page +"_page_next']").attr("disabled", false).val(dataList['next']);	
	  }else{
	   	  $("button[name='"+ page +"_page_next']").attr("disabled", true).val();
	  }
	  if (dataList['previous']){
	   	  $("button[name='"+ page +"_page_previous']").attr("disabled", false).val(dataList['previous']);	
	  }else{
	   	  $("button[name='"+ page +"_page_previous']").attr("disabled", true).val();
	  } 		  
	});
}

function batchManageChoiceAssets(dataList, title, content, type){
	var serverId = [];
	let ips = '' 
	for (var i=0; i <dataList.length; i++){
		serverId.push(dataList[i]["id"])
		ips = ips + dataList[i]["detail"]['ip'] + ' '
	}
  	if (serverId.length > 0){
	    $.confirm({
	        type: 'red',
	        title: title,
	        content: content + ips,
	        buttons: {
	            '确定': {
	                btnClass: 'btn-blue',
	                action: function() {
						$.ajax({
							  type: type,
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
									RefreshAssetsTable("assetsListTable","/api/assets/", "page")
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
							  },
							  error:function(response){
								new PNotify({
									title: 'Ops Failed!',
									text: '批量操作失败',
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
		    title: '批量操作资产',
		    content: '请至少选择一个资产!',
		    type: 'red',
		});	 
  	}	
}

$(document).ready(function() {

	$("button[name^='assets_page_']").on("click", function(){
	   var url = $(this).val();
	   $(this).attr("disabled",true);
	   if (url.length){
	     RefreshAssetsTable('assetsListTable', url, 'assets');
	   }      	
	   $(this).attr('disabled',false);
	}); 	
	
	if($("#assetsListTable").length){
	    function makeAssetsTableList(dataList){
	        var columns = [		                       
	    		           {
	   		                "orderable": false,
	   		                "data":      null,
	   		                "className": 'select-checkbox', 
	   		                "defaultContent": ''
	    		           },  
	                       {
							"className": 'details-control',
							"orderable": false,
							"data":      null,
							"defaultContent": ''
	                       },	
//		                   {"data": "status"},
		                   {"data": "name"},
	                       {"data": "assets_type"},		                       
	                       {"data": "detail.ip"},     
	                       {
	                    	   "data": "detail.system",
	                    	   "defaultContent": ''
	                       },
	    	               {
	                    	   "data": "detail.kernel",
	                    	   "defaultContent": ''
	    	               },
	    	               {
	    	            	   "data": "detail.vcpu_number",
	    	            	   "defaultContent": ''
	    	               },
	    	               {
	    	            	   "data": "detail.ram_total",
	    	            	   "defaultContent": ''
	    	               },
	    	               {
	    	            	   "data": "detail.disk_total",
	    	            	   "defaultContent": ''
	    	               },
	    	               {
	    	            	   "data": "idc_name",
	    	            	   "defaultContent": ''
	    	               }
	    	               ]
	       var columnDefs = [     
	    	    		       {
	       	    				targets: [3],
	       	    				render: function(data, type, row, meta) {  	    					
	       	                        	return formart_assets_type(row.assets_type)
	       	    					}
	    	    		        },	       
	    	    		        {
	       	    				targets: [11],
	       	    				render: function(data, type, row, meta) {  	    					
	       	                        return '<div class="btn-group  btn-group-sm">' +	
				       	                     	'<button type="button" name="btn-assets-alter" value="'+ row.id +'" class="btn btn-default" aria-label="Center Align"><a href="/assets/manage/?id='+row.id+'&model=edit" target="view_window"><span class="glyphicon glyphicon-check" aria-hidden="true"></span></a>' +
					                            '</button>' +
					                            '<button type="button" name="btn-assets-info" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align" data-toggle="modal" data-target=".bs-example-modal-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>' +
					                            '</button>' +	                            
					                            '<button type="button" name="btn-assets-update" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align"><span class="fa fa-refresh" aria-hidden="true"></span>' +
					                            '</button>' +
					                            '<button type="button" name="btn-assets-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +
					                            '</button>' +
	    	    	                           '</div>';
	       	    				},
	       	    				"className": "text-center",
	    	    		        },
	    	    		      ]	
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
						        text: '<span class="fa fa-trash-o"></span>',
						        className: "btn-sm",
						        action: function ( e, dt, node, config ) {  
					            	let dataList = dt.rows('.selected').data()
					            	if (dataList.length==0){
					            		$.alert({
					            		    title: '操作失败',
					            		    content: '批量删除资产失败，请先选择资产',
					            		    type: 'red',		    
					            		});	            		
					            	}else{ 
					            		batchManageChoiceAssets(dataList, '批量删除', '批量删除资产：' ,'DELETE')
					            	} 						        	
						        }
						    },	
						    {
						        text: '更新',
						        className: "btn-sm",
						        action: function ( e, dt, node, config ) {        	
						            	let dataList = dt.rows('.selected').data()
						            	if (dataList.length==0){
						            		$.alert({
						            		    title: '操作失败',
						            		    content: '批量更新资产失败，请先选择资产',
						            		    type: 'red',		    
						            		});	            		
						            	}else{ 
						            		batchManageChoiceAssets(dataList, '批量更新', '批量更新资产：' ,'POST')
						            	} 
						        	} 
						    	},      
						        {
						            text: '全选',
						            className: "btn-sm",
						            action: function (e, dt, button, config) {
						            	dt.rows().select();
						            }
						        },        
						        {
						            text: '反选',
						            className: "btn-sm",
						            action: function (e, dt, button, config) {
						            	dt.rows().deselect();
						            }
						        } ,	  					    
		    ]   
	    	InitDataTableAssets('assetsListTable',dataList,buttons,columns,columnDefs,"assets");	
	    }		    
	    makeAssetsTableList(requests("get","/api/assets/"))		
	    $('#assetsListTable tbody').on('click', 'td.details-control', function () {
	    	var table = $('#assetsListTable').DataTable();
	    	var data ={};
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );
	        aId = row.data()["id"];
		    $.ajax({
		         url : "/api/assets/"+aId+"/",
		         type : "get",
		         async : false,
		         dataType : "json",
		         success : function(result) {
		           	data = result
		         }
		        });	        
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( format(data) ).show();
	            tr.addClass('shown');
	        }
	    });			
		
	}
	
    $('#assetsListTable tbody').on('click','button[name="btn-assets-delete"]',function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var ip = td.eq(4).text();  
		$.confirm({
		    title: '删除确认',
		    content: "确认删除【<strong>"+ip+"</strong>】?",
		    type: 'red',
		    buttons: {
		        删除: function () {
				    	$.ajax({  
				            cache: true,  
				            type: "DELETE",  
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
				            	RefreshAssetsTable("assetsListTable","/api/assets/","assets")
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
    	var ip = td.eq(4).text();  
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
				            	RefreshAssetsTable("assetsListTable","/api/assets/","assets")			            		
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
    	var ip = td.eq(4).text();     	
    	$.ajax({  
            cache: true,  
            type: "GET",  
            url:"/api/assets/"+ vIds +"/",  
            async: false,  
            error: function(response) {  
            	console.log(response)
            },  
            success: function(response) {   	
            	if (Object.keys(response).length > 0){
            		switch (response["status"])
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
							                         ' <td>'+ response["assets_type"] +'</td>' +
							                          '<td> 资产编号  :</td>' +
							                          '<td>'+ response["name"] +'</td>' +			                         
							                        '</tr>' +
							                        '<tr>' +
							                          '<td>设备序列号 :</td>' +
							                          '<td>'+ response["sn"] +'</td>' +
							                          '<td>购买日期 : </td>' +
							                          '<td>'+ response["buy_time"] +'</td>' +			                          
							                        '</tr>' +		
							                        '<tr>' +
							                          '<td>过保日期 :</td>' +
							                          '<td>'+ response["expire_date"] +'</td>' +
							                          '<td>管理IP:</td>' +
							                          '<td>'+ response["management_ip"] +'</td>' +			                          
							                        '</tr>' +
							                        '<tr>' +
							                          '<td>购买人 : </td>' +
							                          '<td>'+ response["buy_user"] +'</td>' +
							                          '<td>生产制造商  :</td>' +
							                          '<td>'+ response["manufacturer"] +'</td>' +			                          
							                        '</tr>' +		
							                        '<tr>' +
							                          '<td>设备型号 :</td>' +
							                          '<td>'+ response["model"] +'</td>' +
							                          '<td>供货商 : </td>' +
							                          '<td>'+ response["provider"] +'</td>' +			                          
							                        '</tr>' +	
							                        '<tr>' +
							                          '<td>放置区域 :</td>' +
							                          '<td>'+ response["idc_name"] +'</td>' +
							                          '<td>机柜信息 : </td>' +
							                          '<td>'+ response["cabinet"] +'</td>' +			                          
							                        '</tr>' +	
							                        '<tr>' +
							                          '<td>设备状态 : </td>' +
							                          '<td>'+ status +'</td>' +
							                          '<td>使用组 :</td>' +
							                          '<td>'+ response["group"] +'</td>' +			                          
							                        '</tr>' +
//							                        '<tr>' +
//							                          '<td>所属项目 : </td>' +
//							                          '<td>'+ response["business"] +'</td>' +
//							                          '<td>所属应用 : </td>' +
//							                          '<td>'+ response["service"] +'</td>' +			                          
//							                        '</tr>' +			                        
							                      '</tbody>' +
							                    '</table>' +							
											'</div>' +
										  '</div>' +
										'</li>';
            		if (Object.keys(response["detail"]).length > 0){
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
			                         ' <td>'+ response["detail"]["hostname"] +'</td>' +
			                          '<td>操作系统:</td>' +
			                          '<td>'+ response["detail"]["system"]+'</td>' +			                         
			                        '</tr>' +
			                        '<tr>' +
			                          '<td>内核版本 :</td>' +
			                          '<td>'+ response["detail"]["kernel"] +'</td>' +
			                          '<td>IP地址 : </td>' +
			                          '<td>'+ response["detail"]["ip"] +'</td>' +			                          
			                        '</tr>' +		
			                        '<tr>' +
			                          '<td>CPU :</td>' +
			                          '<td>'+ response["detail"]["cpu"] +'</td>' +
			                          '<td>CPU个数:</td>' +
			                          '<td>'+ response["detail"]["vcpu_number"] +'</td>' +			                          
			                        '</tr>' +
			                        '<tr>' +
			                          '<td>硬盘大小(GB) : </td>' +
			                          '<td>'+ response["detail"]["disk_total"] +'</td>' +
			                          '<td>Raid类型:</td>' +
			                          '<td>'+ response["detail"]["raid"] +'</td>' +			                          
			                        '</tr>' +		
			                        '<tr>' +
			                          '<td>出口线路 :</td>' +
			                          '<td>'+ response["detail"]["line"] +'</td>' +
			                          '<td>内存容量 (GB): </td>' +
			                          '<td>'+ response["detail"]["ram_total"] +'</td>' +			                          
			                        '</tr>' +	
			                        '<tr>' +
			                          '<td>Swap容量:</td>' +
			                          '<td>'+ response["detail"]["swap"] +'</td>' +
			                          '<td>Selinux : </td>' +
			                          '<td>'+ response["detail"]["selinux"] +'</td>' +			                          
			                        '</tr>' +				                        
			                      '</tbody>' +
			                    '</table>' +							
							'</div>' +
						  '</div>' +
						'</li>';            			
            		}
            		if (Object.keys(response["networkcard"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["networkcard"].length; i++){
		                      if (response["networkcard"][i]["active"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["networkcard"][i]["device"] +'</td>' +
					                          '<td>'+ response["networkcard"][i]["macaddress"]+'</td>' +	
						                      '<td>'+ response["networkcard"][i]["ip"] +'</td>' +
						                      '<td>'+ response["networkcard"][i]["module"]+'</td>' +			
						                      '<td>'+ response["networkcard"][i]["mtu"]+'</td>' +
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
            		if (Object.keys(response["ram"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["ram"].length; i++){
		                      if (response["ram"][i]["device_status"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["ram"][i]["device_model"] +'</td>' +
					                          '<td>'+ response["ram"][i]["device_volume"]+'</td>' +	
						                      '<td>'+ response["ram"][i]["device_brand"] +'</td>' +
						                      '<td>'+ response["ram"][i]["device_slot"]+'</td>' +			
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
            		if (Object.keys(response["disk"]).length > 0){
            			var trTags = '';
						for (var i=0; i <response["disk"].length; i++){
		                      if (response["disk"][i]["device_status"]>0){
		                    	  status = '<td><span class="label label-success">on</span></td>' 
		                      }else{
		                    	  status = '<td><span class="label label-danger">off</span></td>'  
		                      }								
							trTags = trTags + '<tr>' +
					                          '<td>'+ response["disk"][i]["device_model"] +'</td>' +
					                          '<td>'+ response["disk"][i]["device_volume"]+'</td>' +	
					                          '<td>'+ response["disk"][i]["device_serial"] +'</td>' +
						                      '<td>'+ response["disk"][i]["device_brand"] +'</td>' +
						                      '<td>'+ response["disk"][i]["device_slot"]+'</td>' +			
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
		$("#myWebsshModalLabel").html('<p class="text-blank"><code><i class="fa fa fa-terminal"></i></code>'+td.eq(2).text()+'</p>')
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
	            url:"/account/user/manage/",  
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
	
	if($("#modf_user_profile_btn").length){
		$("#modf_user_profile_btn").on("click", function(){
			var vIds = $(this).val();
	    	$.ajax({  
	            type: "POST",  
	            url:"/account/user/manage/",   
				data:{
					"type":"modf_user_profile",
					"id":vIds,
	            	"email":$("#email").val(),
	            	"mobile":$("#mobile").val(),
	            	"name":$("#name").val(),
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