var language =  {
	"sProcessing" : "处理中...",
	"sLengthMenu" : "显示 _MENU_ 项结果",
	"sZeroRecords" : "没有匹配结果",
	"sInfo" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
	"sInfoEmpty" : "显示第 0 至 0 项结果，共 0 项",
	"sInfoFiltered" : "(由 _MAX_ 项结果过滤)",
	"sInfoPostFix" : "",
	"sSearch" : "搜索: ",
	"sUrl" : "",
	"sEmptyTable" : "表中数据为空",
	"sLoadingRecords" : "载入中...",
	"sInfoThousands" : ",",
	"oPaginate" : {
		"sFirst" : "首页",
		"sPrevious" : "上页",
		"sNext" : "下页",
		"sLast" : "末页"
	},
	"oAria" : {
		"sSortAscending" : ": 以升序排列此列",
		"sSortDescending" : ": 以降序排列此列"
	}
}

function orderInfoFormat(dataList) {
	if (dataList["order_type"]==2){
	    var trHtml = '';
		for (var i=0; i <dataList["detail"]["files"].length; i++){	
		    trHtml += '<tr><td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["files"][i]["file_path"] +'</td>'+ '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["files"][i]["file_type"] +'</td></tr>'	    
		};
		var uploadHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
			    			'<legend>工单明细</legend>' +
			    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			    				'<tr>' +
			    					'<th>目标路径</th>' +
			    					'<th>工单内容</th>' +
			    					'<th>目标服务器</th>' +
			    					'<th>宿主</th>' +
			    					'<th>权限</th>' +
			    					'<th>取消原因</th>' +
			    				'</tr>' + 
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["upload"]["dest_path"] +'</td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_content-'+dataList["id"]+'">'+dataList["detail"]["upload"]["order_content"].substring(-1,10)+'...</a></td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_server-' +dataList["id"]+'">'+dataList["detail"]["upload"]["server"][0].substring(-1,10)+'...</a></td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["upload"]["chown_user"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["upload"]["chown_rwx"] +'</td>' +
								  	'<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_cancel"] +'</td>' +
							  	 '</tr>' +		    				
			    				'</table>' +
		    				'</div>'; 	
			
	    var fileHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		    				'<legend>文件信息</legend>' +
		    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
			    				'<tr>' +
			    					'<th>文件名称</th>' +
			    					'<th>文件类型(检测)</th>' +
		    					'</tr>'	+    				
			    				 trHtml  +
		    				'</table>' +
	    				'</div>'; 	
	    return '<div class="row">'+ uploadHtml + '</div><div class="row">' +  fileHtml + '</div>';
	}else if(dataList["order_type"]==0){  
		if(dataList["detail"]["sql"]["order_err"]){
			var err = '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-err-'+dataList["id"]+'">'+dataList["detail"]["sql"]["order_err"].substring(-1,10)+'...</a></td>'
		}else{
			var err = '<td class="col-md-1 col-sm-12 col-xs-12">无</td>'
		}
		var sqlHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
			    			'<legend>工单明细</legend>' +
			    				'<table class="table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			    				'<tr>' +
			    					'<th>SQL类型</th>' +
			    					'<th>SQL内容</th>' +
			    					'<th>错误信息</th>' +
			    					'<th>是否备份</th>' +
			    					'<th>取消原因</th>' +
			    				'</tr>' + 
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12"><code>'+ orderSQLtypeJson[dataList["detail"]["sql"]["order_type"]] +'</code></td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-sql-'+dataList["id"]+'">'+dataList["detail"]["sql"]["order_sql"].substring(-1,10)+'...</a></td>' +
								  	  err +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ orderBackupHmtl[dataList["detail"]["sql"]["sql_backup"]] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_cancel"] +'</td>' +
							  	 '</tr>' +		    				
			    				'</table>' +
		    				'</div>'; 	
			
	    var dbHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		    				'<legend>目标数据库</legend>' +
		    				'<table class="table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
			    				'<tr>' +
			    					'<th>环境</th>' +
			    					'<th>数据库</th>' +
			    					'<th>数据库地址</th>' +
			    					'<th>端口</th>' +
		    					'</tr>'	+    				
			    				'</tr>' + 
									 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dbEnvHtml[dataList["detail"]["db"]["db_env"]] +'</td>'+ 
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["db_name"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["host"] +'</td>' +
								  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["db"]["db_port"] +'</td>' +
							  	 '</tr>' +
		    				'</table>' +
	    				'</div>'; 
	    return '<div class="row">'+ sqlHtml + '</div><div class="row">' +  dbHtml + '</div>';
	}else if(dataList["order_type"]==3){
		var downloadHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
		'<legend>工单明细</legend>' +
			'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
			'<tr>' +
				'<th>目标路径</th>' +
				'<th>工单内容</th>' +
				'<th>目标服务器</th>' +
				'<th>取消原因</th>' +
			'</tr>' + 
			'</tr>' + 
				 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["detail"]["download"]["dest_path"] +'</td>'+ 
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_content-'+dataList["id"]+'">'+dataList["detail"]["download"]["order_content"].substring(-1,10)+'...</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12"><a data-toggle="modal" id="tooltips-order_server-' +dataList["id"]+'">'+dataList["detail"]["download"]["server"][0].substring(-1,10)+'...</a></td>' +
			  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["order_cancel"] +'</td>' +
		  	 '</tr>' +		    				
			'</table>' +
		'</div>'; 	

		return '<div class="row">'+ downloadHtml + '</div>';
	}			
}

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
}

function requests(method,url,data){
	var ret = '';
	$.ajax({
		async:false,
		url:url, //请求地址
		type:method,  //提交类似
       	success:function(response){
             ret = response;
        },
        error:function(data){
            ret = {};
        }
	});	
	return 	ret
}

var orderMode = {
    "0":'邮箱',
    "1":'微信',         
    "2":'钉钉',		
}

var userInfo = {
		
}



var orderStatusHtml = {
	"0":'<span class="label label-success">已通过</span>',
    "1":'<span class="label label-danger">已拒绝</span>',
    "2":'<span class="label label-info">审核中</span>',
    "3":'<span class="label label-success">已部署</span> ',
    "4":'<span class="label label-info">待授权</span>',
    "5":'<span class="label label-success">已执行</span>',
    "6":'<span class="label label-default">已回滚</span>',
    "7":'<span class="label label-danger">已撤回</span>',
    "8":'<span class="label label-warning">已授权</span>',
    "9":'<span class="label label-danger">已失败</span>',	
}

var orderTypeHtml = {
	"0":'<span class="label label-info">SQL更新</span>',
	"1":'<span class="label label-success">代码更新</span>',
	"2":'<span class="label label-warning">文件分发</span>',
	"3":'<span class="label label-danger">文件下载</span>'
}

var orderTypeJson = {
	"0":'sql',
	"1":'deploy',
	"2":'fileupload',
	"3":'filedownload'		
}

var orderSQLtypeJson = {
	"online":"工具审核",
	"file":"SQL文件",
	"human":"人工审核"
}

var dbEnvHtml = {
	"beta":'<span class="label label-success">测试环境</span>',	
	"ga":'<span class="label label-danger">生产环境</span>',	
}

var orderBackupHmtl = {
	"0":'<span class="label label-warning">无备份</span>',	
	"1":'<span class="label label-success">有备份</span>',
}

function InitDataTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
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
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
	  });
	  if (data['next']){
		  $("button[name='page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='page_previous']").attr("disabled", true).val();
	  }	  

}

function RefreshOrdersTable(tableId, urlData){
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
	   	  $("button[name='page_next']").attr("disabled", false).val(dataList['next']);	
	  }else{
	   	  $("button[name='page_next']").attr("disabled", true).val();
	  }
	  if (dataList['previous']){
	   	  $("button[name='page_previous']").attr("disabled", false).val(dataList['previous']);	
	  }else{
	   	  $("button[name='page_previous']").attr("disabled", true).val();
	  } 	  
	});
}

function InitDataConfigTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
}

function RefreshConfigTable(tableId, urlData){
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

$(document).ready(function() {
	
	
	var groupList = requests("get","/api/group/")
	$(function() {
		if($('#grant_group').length){
			var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="grant_group" id="grant_group"  autocomplete="off"><option selected="selected" value="">选择一个授权组</option>'
			var selectHtml = '';
			for (var i=0; i <groupList.length; i++){
				selectHtml += '<option value="'+ groupList[i]["id"] +'">'+ groupList[i]["name"] +'</option>' 					 
			};                        
			binlogHtml =  binlogHtml + selectHtml + '</select>';
			document.getElementById("grant_group").innerHTML= binlogHtml;							
			$('#grant_group').selectpicker('refresh');					
		}
	})	
	
	$("button[name='noticeonfig']").on("click", function(){
		var vIds = $(this).val();
		if (vIds > 0){
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/'+vIds+'/', //请求地址
				type:"PUT",  //提交类似
				data:{
					"order_type":$('#order_type option:selected').val(),
					"mode":$('#mode option:selected').val(),
					"grant_group":$('#grant_group option:selected').val(),
					"number":$("#number").val()
				}, //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '修改成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
				},
		    	error:function(response){
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });  
		    	}
			})			
		}else{
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/', //请求地址
				type:"POST",  //提交类似
				data:$("#order_config").serialize(), //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
				},
		    	error:function(response){
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });  
		    	}
			})				
		}
	})
	
	function makeConfigList(){
		var groupData = {}
		for (var i=0; i <groupList.length; i++){	
			groupData[groupList[i]["id"]] = groupList[i]["name"]
		}
	    var columns = [
	                   	{"data": "id","className": "text-center",},
	                    {"data": "order_type","className": "text-center",},
	                    {"data": "grant_group","className": "text-center",},	
	                    {"data": "mode","className": "text-center",},
	                    {"data": "number","className": "text-center",},
		               ]
	    var columnDefs = [		
	   	    		        {
	    	    				targets: [1],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	    					return orderTypeHtml[row.order_type]
	    	    				},
	    	    				"className": "text-center",
   	    		        },	    
   	    		        {
    	    				targets: [2],
    	    				render: function(data, type, row, meta) {		    	    					
    	    					return '<strong>'+orderMode[row.mode]+'</strong>'
    	    				},
    	    				"className": "text-center",
	    		        },  
   	    		        {
    	    				targets: [3],
    	    				render: function(data, type, row, meta) {		    	    					
    	    					return groupData[row.grant_group]
    	    				},
    	    				"className": "text-center",
	    		        },	    		        
   	    		        {
	    	    				targets: [5],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-config-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-config-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
		    	                           '</button>' +			                            
		    	                           '</div>';
	    	    				},
	    	    				"className": "text-center",
   	    		        },
   	    		      ]	
        var buttons = [{
            text: '<span class="fa fa-plus"></span>',
            className: "btn-xs",
            action: function ( e, dt, node, config ) {
            	addCategory()
            }
        }]
		InitDataConfigTable('configList',"/api/orders/notice/",buttons,columns,columnDefs)
	}	  
	makeConfigList()	
	
    $('#configList tbody').on('click',"button[name='btn-config-edit']", function(){
    	var vIds = $(this).val();    	
		$.ajax({
			dataType: "JSON",
			url:'/api/orders/notice/'+vIds+'/', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				DynamicSelect("order_type",response["order_type"])	
				$("#order_type").prop('disabled', true);
				DynamicSelect("grant_group",response["grant_group"])	
				DynamicSelect("mode",response["mode"])
				$("#number").val(response["number"])
				$('.selectpicker').selectpicker('refresh');	
				$("button[name='noticeonfig']").val(vIds).text("修改")
			},
	    	error:function(response){
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });  
	    	}
		})    	
    })	

    $('#configList tbody').on('click',"button[name='btn-config-delete']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var name = td.eq(1).text(); 
    	var mode = td.eq(2).text();
		$.confirm({
		    title: '删除确认',
		    content: "确认删除:【"+ name +"】使用<strong>"+mode+"</strong>发送通知方式？",
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            type: "DELETE",  
		            url:'/api/orders/notice/'+vIds+'/',  
		            error: function(response) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });       
		            },  
		            success: function(response) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshConfigTable('configList', '/api/orders/notice/')
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		}) 	
    })  	
	
	
	var userList = requests("get","/api/user/")
	for (var i=0; i <userList.length; i++){
		userInfo[userList[i]["id"]] = userList[i]
	}
    if ($("#ordersLists").length) {
    	
        $("button[name^='page_']").on("click", function(){
          	var url = $(this).val();
          	$(this).attr("disabled",true);
          	if (url.length){
          		RefreshOrdersTable('ordersLists', url);
          	}      	
        	$(this).attr('disabled',false);
          }); 
    	
    	var currentUser = $("#currentUser").val()
    	
    	function makeOrderTableList(){
		    var columns = [
		                   	{
		                   		"className":      'details-control',
			                    "orderable":      false,
			                    "data":           null,
			                    "defaultContent": ''
			                },		                   
		                    {"data": "id"},
		                    {"data": "order_type"},
		                    {"data": "order_user"},
			                {"data": "order_subject"},
			                {"data": "order_executor"},	
			                {"data": "create_time"},	
			                {"data": "order_status","className": "text-center",},	
			                {"data": "modify_time"},			                			                
			               ]
		    var columnDefs = [			                      
								{
									targets: [2],
									render: function(data, type, row, meta) {
										return orderTypeHtml[row.order_type]
									},
								},
								{
									targets: [3],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_user]["username"]
									},
								},
								{
									targets: [5],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_executor]["username"]
									},
								},	
								{
									targets: [7],
									render: function(data, type, row, meta) {
								        return orderStatusHtml[row.order_status]
									},
								},								
	    	    		        {
		    	    				targets: [9],
		    	    				render: function(data, type, row, meta) {	
		    	    					if (row.order_status==4 || row.order_status==2){
		    	    						/*如果是工单状态是待授权或者审核中，则开启授权功能*/
			    	    					if (currentUser==row.order_executor || userInfo[currentUser]["is_superuser"]){
			    	    						/*如果是工单执行人或者超级管理员授权*/
			    	    						var grant = '<button type="button" name="btn-order-grant" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-check" aria-hidden="true"></span></button>'
			    	    					}else{
			    	    						var grant = '<button type="button" name="btn-order-grant" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" disabled><span class="fa fa-check" aria-hidden="true"></span></button>'
			    	    					}		    	    						
		    	    					}else{
		    	    						var grant = '<button type="button" name="btn-order-grant" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" disabled><span class="fa fa-check" aria-hidden="true"></span></button>'
		    	    					}
		    	    					/*----------*/
		    	    					if (userInfo[currentUser]["is_superuser"]){
		    	    						/*超级管理员才能删除工单*/
		    	    						var dels = '<button type="button" name="btn-order-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var dels = ''
		    	    					}
		    	    					/*----------*/
		    	    					if (row.order_status==4 || row.order_status==8){
		    	    						/*如果是工单状态是待授权或者已授权，则开启取消功能*/
		    	    						var cancel = '<button type="button" name="btn-order-cancel" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-times" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var cancel = '<button type="button" name="btn-order-cancel" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" disabled><span class="fa fa-times" aria-hidden="true"></span></button>'
		    	    					}
		    	    					/*----------*/
		    	    					switch(row.order_type)
		    	    					{
		    	    					case 0:
		    	    						var url = '/order/sql/handle/?type=sql&&id='+row.id
		    	    					  break;
		    	    					case 2:
		    	    						var url = '/order/fileupload/handle/?type=fileupload&&id='+row.id
		    	    					  break;
		    	    					case 3:
		    	    						var url = '/order/filedownload/handle/?type=filedownload&&id='+row.id
		    	    					  break;		    	    						
		    	    					default:
		    	    						var url = '/order/apps/handle/?type=deploy&&id='+row.id
		    	    					}
		    	                        return '<div class="btn-group  btn-group-sm">' +	
			    	                           '<button type="button" name="btn-order-run" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><a href="'+url+'"><span class="fa fa-play-circle-o" aria-hidden="true"></span></a>' +	
			    	                           '</button>' + grant + cancel + dels + 			                            
			    	                           '</div>';
		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    var buttons = [
						    {
						        text: '<span class="fa fa-cogs"></span>',
						        className: "btn-sm",
						        action: function ( e, dt, node, config ) {        	
		    	                    if($('#noticeConfigDiv').is(':hidden')){
		    	                    	$('#noticeConfigDiv').show();
		    	                    }
		    	                    else{
		    	                    	$('#noticeConfigDiv').hide();
		    	                    } 						        	
						        }
						    },		                   
		                   {
					        text: '<span class="fa fa-cubes"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) { 
					        	window.open('/order/apply/')
					        }
					    },
					    {
					        text: '<span class="fa fa-cloud-upload"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },	
					    {
					        text: '<span class="fa fa-cloud-download"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },						    
					    
		    ] 		    
		    InitDataTable('ordersLists','/api/orders/list/',buttons,columns,columnDefs);   		
    	}
    	
    	makeOrderTableList()
    	
    	var table = $('#ordersLists').DataTable();
    	
    	$('#ordersLists tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );	        
	        aId = row.data()["id"];
	        order_type = row.data()["order_type"]
	        $.ajax({
	            url : "/order/info/?type="+ orderTypeJson[order_type] +"&&id="+aId,
	            type : "get",
	            async : false,
	            success : function(result) {
	            	dataList = result.data;
	            }
	        });	        
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( orderInfoFormat(dataList) ).show();
	            tr.addClass('shown');
	        }
	        switch(order_type)
	        {
	        case 0:
		        $('#tooltips-sql-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["sql"]["order_sql"].replace(/;/g, ";<br>") 
		        }); 
		        $('#tooltips-err-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["sql"]["order_err"].replace(/;/g, ";<br>") 
		        });
	          break;
	        case 2:
	        	var server = ''
	        	for (var i=0; i <dataList["detail"]["upload"]["server"].length; i++){
	        		server += dataList["detail"]["upload"]["server"][i] + ';'
	        	}
		        $('#tooltips-order_content-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["upload"]["order_content"]
		        });	
		        $('#tooltips-order_server-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: server.replace(/;/g, "<br>") 
		        });	        
	          break;
	        case 3:
	        	var server = ''
		        	for (var i=0; i <dataList["detail"]["download"]["server"].length; i++){
		        		server += dataList["detail"]["download"]["server"][i] + ';'
		        	}
			        $('#tooltips-order_content-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: dataList["detail"]["download"]["order_content"]
			        });	
			        $('#tooltips-order_server-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: server.replace(/;/g, "<br>") 
			        });	 	        	
	          break;
	        default:
	          break;
	        }         
	    });	
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-cancel"]',function(){
    		var vIds = $(this).val();
    		orderInfo = $(this).parent().parent().parent().find("td")
    		username =  orderInfo.eq(3).text()
    		order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-times',
    	        type: 'red',
    	        title: '取消<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单?',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
    			            '<div class="form-group">' +
    			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">取消说明<span class="required">*</span>' +
    			              '</label>' +
    			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
    			              	'<input type="text"  name="modf_order_cancel" value="" required="required" class="form-control col-md-7 col-xs-12">' +
    			              '</div>' +                                           			
    			          '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                    var cancel = this.$content.find("[name='modf_order_cancel']").val();
    				    	$.ajax({  
    				            cache: true,  
    				            type: "PUT",  
    				            url:"/api/orders/" + vIds + '/',  
    				            data:{
    				            	"order_cancel":cancel,
    				            	"order_status":7,
    				            	},
    				            error: function(request) {  
    				            	new PNotify({
    				                    title: 'Ops Failed!',
    				                    text: request.responseText,
    				                    type: 'error',
    				                    styling: 'bootstrap3'
    				                });       
    				            },  
    				            success: function(data) {  
    				            	new PNotify({
    				                    title: 'Success!',
    				                    text: '工单取消成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshOrdersTable('ordersLists','/api/orders/list/')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	 
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-grant"]',function(){
    		var vIds = $(this).val();
    		orderInfo = $(this).parent().parent().parent().find("td")
    		username =  orderInfo.eq(3).text()
    		order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'blue',
    	        title: '确认授权<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单?',
    	        content: '',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    				    	$.ajax({  
    				            cache: true,  
    				            type: "PUT",  
    				            url:"/api/orders/" + vIds + '/',  
    				            data:{
    				            	"order_status":8,
    				            	},
    				            error: function(request) {  
    				            	new PNotify({
    				                    title: 'Ops Failed!',
    				                    text: request.responseText,
    				                    type: 'error',
    				                    styling: 'bootstrap3'
    				                });       
    				            },  
    				            success: function(data) {  
    				            	new PNotify({
    				                    title: 'Success!',
    				                    text: '工单授权成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshOrdersTable('ordersLists','/api/orders/list/')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	  
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-delete"]',function(){
    		var vIds = $(this).val();
    		orderInfo = $(this).parent().parent().parent().find("td")
    		username =  orderInfo.eq(3).text()
    		order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'red',
    	        title: '确认删除<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单?',
    	        content: '',
    	        buttons: {
    	            '取消': function() {},
    	            '删除': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    				    	$.ajax({  
    				            cache: true,  
    				            type: "DELETE",  
    				            url:"/api/orders/" + vIds + '/',  
    				            error: function(request) {  
    				            	new PNotify({
    				                    title: 'Ops Failed!',
    				                    text: request.responseText,
    				                    type: 'error',
    				                    styling: 'bootstrap3'
    				                });       
    				            },  
    				            success: function(data) {  
    				            	new PNotify({
    				                    title: 'Success!',
    				                    text: '工单删除成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	RefreshOrdersTable('ordersLists','/api/orders/list/')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	  	
    	
	}
    
	
})