
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
						if (data["detail"]["order_type"]=='online' && $.isArray(response["data"]["order_audit_status"])){
							makeSQLresult('auditResult',response["data"]["result"])
							$("#order_audit_status").html(orderAuditStatusHtml[response["data"]["order_audit_status"]])
							$("#audit_sql_btn").attr("disabled",true)
							queryOsc()
						}
						else if (data["detail"]["order_type"]=='file' || data["detail"]["order_type"]=='human'){
							$("#order_audit_status").html(orderAuditStatusHtml[response["data"]["order_audit_status"]])
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