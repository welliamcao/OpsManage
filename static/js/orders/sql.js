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

function get_url_param(name) {
	 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	 var r = window.location.search.substr(1).match(reg);
	 if (r != null) return unescape(r[2]); return null; 
}

var orderAuditStatusHtml = {
	    "1":'<span class="label label-danger">已拒绝</span>',
	    "2":'<span class="label label-info">审核中</span>',
	    "3":'<span class="label label-success">已授权</span> '
	}

var orderExecuteStatusHtml = {
		"0":'<span class="label label-warning">已提交</span>',
	    "1":'<span class="label label-info">处理中</span>',
	    "2":'<span class="label label-success">已完成</span>',
	    "3":'<span class="label label-warning">已回滚</span> ',
	    "4":'<span class="label label-default">已关闭</span> ',
	    "5":'<span class="label label-danger">执行失败</span> ',
	}

function makeSQLresult(ids,dataList){
	$("#auditResultDiv").show()
	if ($.isArray(dataList)){		
		var resultHTML =  '<table class="table table-hover" id="auditResult">' +
	    '<thead>' +
	        '<tr>' +
	            '<th>#</th>' +
	            '<th>SQL</th>' +
	            '<th>影响行</th>' +
	            '<th>错误原因</th>' +
	        '</tr>' +
		'</thead>' +
		'<tbody>'
	     var trHtml = ''
	     for (var i=0;i< dataList.length;i++){
	    	 trHtml +=   '<tr>' + 
	                         '<td>'+ i +'</td>' + 
	                         '<td>'+ dataList[i]['sqltext'] +'</td>' + 
	                         '<td>'+ dataList[i]['affectrow'] +'</td>' + 
	                         '<td>'+ dataList[i]['errormessage'] +'</td>' + 
	                     '</tr>'
	     }
		resultHTML = resultHTML + trHtml + '</tbody></table>'
		$('#'+ids).html(resultHTML);			
	}else{
		var resultHTML =  '<pre id="auditResult">' + dataList +'</pre>'
		$('#'+ids).html(resultHTML);		
	}
	
}

function queryOsc(){
	var interval = setInterval(function(){  
        $.ajax({  
            url : '/order/info/?type=get_osc&&id='+get_url_param("id"),  
            type : 'get',
            success : function(response){
            	if (response["data"]["status"]=="success"){
                	$("#hasPsc").show()
                	if( response["data"]["data"]["percent"] >= 100 ){      
    					var perHtml = '<div class="form-group" id="osc_per">' +							
    										'<div class="progress progress_sm">' +
                                  				'<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 100%;"></div>' +
                                			'</div>' +			
    								  '</div>' 	
    					var timeHtml = '<code id="osc_time">00:00</code>';
    					var osc_percent = '<code id="osc_percent">100%</code>';
    					document.getElementById("osc_per").innerHTML= perHtml;
    					document.getElementById("osc_time").innerHTML= timeHtml;
    					document.getElementById("osc_percent").innerHTML= osc_percent;
    					$("#stop_osc").attr("disabled", true);
    					clearInterval(interval);
                	}
                	else{
    					var perHtml = '<div class="form-group" id="osc_per">' +							
    										'<div class="progress progress_sm">' +
                                  				'<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: ' + response["data"]["data"]["percent"] + '%;"></div>' +
                                			'</div>' +			
    								  '</div>' 							            			
    					var timeHtml = '<code id="osc_time">' + response["data"]["data"]["timeRemained"] +'</code>'
    					var osc_percent = '<code id="osc_percent">'+ response["data"]["data"]["percent"] +'%</code>'
    					document.getElementById("osc_per").innerHTML= perHtml;
    					document.getElementById("osc_time").innerHTML= timeHtml;
    					document.getElementById("osc_percent").innerHTML= osc_percent;
    					$("#stop_osc").val(get_url_param("id")).attr("disabled", false);
                	}            		
            	}else{
            		clearInterval(interval);
            	}

            },
	    	error:function(response){
	    		clearInterval(interval);
	    	}	            
        });  
    },3000);	
}

function makeSQLrollback(ids,dataList){
	if ($.isArray(dataList)){	
		$("#auditRollbackDiv").show()
		 var resultHTML =  ''
	     for (var i=0;i< dataList.length;i++){
	    	 resultHTML += dataList[i] + '<br>'
	     }
		$('#'+ids).html('<pre>'+resultHTML+'</pre>');			
	}
}

function requests(method,url,async){
	var ret = '';
	if(!async){async=false;} 
	$.ajax({
		async:async,
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

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
	$("#" + ids).attr("disabled","")
	$('#'+ids).selectpicker('refresh');	
}

function makeDatabaseSelect(ids,data){
	if (data["db_env"]=="beta"){
		var beta = "测试环境"
	}else{
		var beta = "生产环境"
	}
	var dbHtml = '<select class="selectpicker form-control"  name="order_db" id="order_db">' +
				    '<option name="order_db" value="'+data["id"]+'" selected="selected">'+ data["db_env"] +' | '+data["ip"]+' | '+data["db_name"]+' | '+data["db_mark"]+'</option>' +
				 '</select>'
	$('#'+ids).html(dbHtml)		
	$("#"+ids).attr("disabled","")
	$('#'+ids).selectpicker('refresh');	
}

function makeUserSelect(ids,dataList){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="'+ ids +'" id="'+ids+'"  autocomplete="off"><option selected="selected" value="">选择一个用户</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]["username"] +'</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$('#'+ids).html(binlogHtml)		
	$('#'+ids).selectpicker('refresh');		
}

function setAceEditMode(model,readOnly) {
	var editor = ace.edit("compile-editor-add");
	require("ace/ext/old_ie");
	var langTools = ace.require("ace/ext/language_tools");
	editor.setTheme("ace/theme/monokai");
	editor.getSession().setMode("ace/mode/" + model);
	editor.setReadOnly(readOnly); 
	editor.setShowPrintMargin(false);
	editor.setOptions({
	    enableBasicAutocompletion: true,
	    enableSnippets: true,
	    enableLiveAutocompletion: true
	}); 
			 
};	

function makeOrderLogsTableList(url){
	if ($('#ordersLogs').hasClass('dataTable')) {
		dttable = $('#ordersLogs').dataTable();
		dttable.fnClearTable(); //清空table
		dttable.fnDestroy(); //还原初始化datatable
	}	
	var data = requests('get',url)
    var columns = [		                   
                    {"data": "order"},
                    {"data": "operator"},
                    {"data": "operation_info"},
                    {"data": "audit_status"},
                    {"data": "execute_status"},
	                {"data": "operation_time"}			                			                
	               ]
    var columnDefs = [			                      
						{
							targets: [3],
							render: function(data, type, row, meta) {
						        return orderAuditStatusHtml[row.audit_status]
							},
						},
						{
							targets: [4],
							render: function(data, type, row, meta) {
						        return orderExecuteStatusHtml[row.execute_status]
							},
						}						
	    		      ]
    
    var buttons = [
			    					    
    ] 		    
    $('#ordersLogs').dataTable({
	    "dom": "Bfrtip",
	    "buttons":buttons,
		"bScrollCollapse": false, 				
	    "bRetrieve": true,			
		"destroy": true, 
		"data":	data,
		"columns": columns,
		"columnDefs" :columnDefs,			  
		"language" : language,
		"order": [[ 0, "desc" ]],
		"autoWidth": false	    			
	});    
}

$(document).ready(function() {
	
	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	
	var data = requests('get','/api/orders/'+get_url_param("id")+'/')
	$(function() {
		$("#order_audit_status").html(orderAuditStatusHtml[data["order_audit_status"]])
		$("#order_time").val(data["start_time"]+' - '+ data["end_time"]).attr("disabled","")
		$("#order_desc").val(data["order_subject"]).attr("disabled","")
		$("#compile-editor-add").text(data["detail"]["order_sql"])
		setAceEditMode("mysql",true);
		makeDatabaseSelect("order_db",data["detail"]["db"])	
		DynamicSelect("sql_backup",data["detail"]["sql_backup"])
		makeUserSelect('order_executor',requests('get','/api/account/user/superior/',false))
		DynamicSelect('order_executor',data["order_executor"])
		if (data["detail"]["order_type"] == "online"){
			
			if (data["order_audit_status"] == 3){
				$("#audit_sql_btn").val(get_url_param("id")).attr("disabled",false)
			}				

			if (data["order_execute_status"] == 2){
				makeSQLresult('auditResult',data["detail"]["result"])
				if (data["detail"]["sql_backup"]==1){
					var rollbackSql = requests('get','/order/info/?type=get_rollback_sql&&id='+get_url_param("id"))
					makeSQLrollback("auditRollback",rollbackSql["data"]["sql"])
					$("#audit_sql_btn").hide();
					$("#rollback_sql_btn").val(get_url_param("id")).text("回滚").attr({"disabled":false});
					$("#rollback_sql_btn").show();
				}	
			}			
			
			if (data["order_execute_status"] == 3){
				var rollbackSql = requests('get','/order/info/?type=get_rollback_sql&&id='+get_url_param("id"))
				makeSQLrollback("auditRollback",rollbackSql["data"]["sql"])
			}		
			
			if (data["order_execute_status"] == 5){
				makeSQLresult('auditResult',data["detail"]["result"])
			}				
			
/*			switch(data["order_audit_status"])
			{
			case 2:
				$("#audit_sql_btn").val(get_url_param("id")).attr("disabled",false)
			  break;
			case 9:
				makeSQLresult('auditResult',data["detail"]["result"])
			  break;
			case 5:
				makeSQLresult('auditResult',data["detail"]["result"])
				if (data["detail"]["sql_backup"]==1){
					var rollbackSql = requests('get','/order/info/?type=get_rollback_sql&&id='+get_url_param("id"))
					makeSQLrollback("auditRollback",rollbackSql["data"]["sql"])
					$("#audit_sql_btn").hide();
					$("#rollback_sql_btn").val(get_url_param("id")).text("回滚").attr({"disabled":false});
					$("#rollback_sql_btn").show();
				}				
			  break;
			case 6:
				var rollbackSql = requests('get','/order/info/?type=get_rollback_sql&&id='+get_url_param("id"))
				makeSQLrollback("auditRollback",rollbackSql["data"]["sql"])
			  break;	
			}	*/		
		}else if(data["detail"]["order_type"] == "file" || data["detail"]["order_type"] == "human"){
			if (data["order_execute_status"]==5){
				makeSQLresult('auditResult',data["detail"]["order_err"])
				return false
			}	
			if (data["order_audit_status"] == 3){
				$("#audit_sql_btn").val(get_url_param("id")).attr("disabled",false)
			}				
		}		
/*		if (data["code"]=="200"){

		}*/
	})
    $("button[name='audit_sql_btn']").on('click', function() {
    	var value = $(this).val();
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		if (value>=1){
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
	            url:"/order/sql/handle/",  
	            data:{
	            	"id":value,
	            	"type":"exec_sql"
	            	},
	            error: function(response) {
	            	btnObj.attr('disabled',false);
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.statusText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });      
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
						if (data["detail"]["order_type"]=='online' && $.isArray(response["data"]["result"])){
							makeSQLresult('auditResult',response["data"]["result"])
							$("#order_audit_status").html(orderAuditStatusHtml[response["data"]["status"]])
							$("#audit_sql_btn").attr("disabled",true)
							queryOsc()
						}
						else if (data["detail"]["order_type"]=='file' || data["detail"]["order_type"]=='human'){
							$("#order_audit_status").html(orderAuditStatusHtml[response["data"]["status"]])
							$("#audit_sql_btn").attr("disabled",true)
							if (response["data"]["result"].length > 0){
					    		$.alert({
					    		    title: '工单执行失败',
					    		    content: response["data"]["result"],
					    		    type: 'red',
					    		});									
							}
						}
					}
					else {
			    		$.alert({
			    		    title: 'SQL上线失败',
			    		    content: response["msg"],
			    		    type: 'red',
			    		});		    		
					};
					makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	            }  
	    	});			
		}
		else{
			console.log(value)
		}
    });	
    
    $("button[name='rollback_sql_btn']").on('click', function() {
    	var value = $(this).val();
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		if (value>=1){
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'red',
    	        title: '确认回滚<strong>'+data["order_subject"]+'</strong>工单?',
    	        content: '',
    	        buttons: {
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	        	    	$.ajax({  
    	        	            cache: true,  
    	        	            type: "POST",  
    	        	            url:"/order/sql/handle/",  
    	        	            data:{
    	        	            	"id":value,
    	        	            	"type":"rollback_sql"
    	        	            	},
    	        	            error: function(response) {
    	        	            	btnObj.attr('disabled',false);
    	        	            	new PNotify({
    	        	                    title: 'Ops Failed!',
    	        	                    text: response.statusText,
    	        	                    type: 'error',
    	        	                    styling: 'bootstrap3'
    	        	                });       
    	        	            },  
    	        	            success: function(response) {  
    	        					if (response["code"] == 200){
    	        						$("#order_audit_status").html(orderExecuteStatusHtml[3])
        				            	new PNotify({
        				                    title: 'Success!',
        				                    text: '工单回滚成功',
        				                    type: 'success',
        				                    styling: 'bootstrap3'
        				                });    	        						
    	        					}
    	        					else {
    	        						btnObj.attr('disabled',false);
    	        			    		$.alert({
    	        			    		    title: 'SQL回滚失败',
    	        			    		    content: response["msg"],
    	        			    		    type: 'red',
    	        			    		});		    		
    	        					};
    	        					makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
    	        	            }  
    	        	    	});
    	                }
    	            },
    	            '取消': function() {
    	            	btnObj.attr('disabled',false);
    	            }
    	        }
    	    });  						
		}
		else{
			console.log(value)
		}
    });    
    
    $("#stop_osc").on('click', function() {
    	var value = $(this).val();
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		if (value>=1){
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
	            url:"/order/sql/handle/",  
	            data:{
	            	"id":value,
	            	"type":"stop_osc"
	            	},
	            error: function(response) {
	            	btnObj.attr('disabled',false);
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });       
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: '任务取消成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 	
					}
					else {
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response["msg"],
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 	    		
					};
					makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	            }  
	    	});			
		}
		else{
			console.log(value)
		}
    });	    
    
})