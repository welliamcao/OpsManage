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

var sched_type_array = {
		"cron":"cron类型",
		"interval":"间隔类型",
		"date":"日期类型" 
}

var sched_notice_type = {
        0:'邮箱',
        1:'微信',         
        2:'钉钉',		
}

var jobsDataList = []

var jobsResults = {}

function checkValue(value){
	if(value){
		return value
	}
	else{
		return ""
	}
}

function format (dataList) {
	var schedHtml = ''
	var nHtml = ''
	if (JSON.stringify(dataList) != '{}'){
		var nHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
					'<legend>告警通知</legend>' +
						'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
						'<tr>' +
							'<th>告警方式</th>' +
							'<th>联系人</th>' +
							'<th>告警间隔</th>' +
							'<th>上次告警时间</th>' +
						'</tr>' +
						'<tr>' +
							'<th>'+ checkValue(sched_notice_type[dataList["alert_detail"]["notice_type"]]) +'</th>' +
							'<th>'+ checkValue(dataList["alert_detail"]["notice_number"]) +'</th>' +
							'<th>'+ checkValue(dataList["alert_detail"]["notice_interval"]) +'</th>' +
							'<th>'+ UnixToDate(dataList["alert_detail"]["atime"]) +'</th>' +
						'</tr>' +						
						'</table>'
					'</div>'; 	
		
		if(dataList["jobs_detail"]["type"]=="cron"){
			var schedHtml = '<tr>'+ 
								'<td>秒</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["second"]) + '</td>'+
							'</tr>' +
							'<tr>'+ 
								'<td>分</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["minute"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>小时</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["hour"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>周</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["week"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["day"]) + '</td>'+
							'</tr>' +
							'<tr>'+ 
								'<td>月</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["month"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>星期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["day_of_week"]) + '</td>'+
							'</tr>' +
							'<tr>'+ 
								'<td>年</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["year"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>开始日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["start_date"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>结束日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["end_date"]) + '</td>'+
							'</tr>'						
		}else if(dataList["jobs_detail"]["type"]=="interval"){
			var schedHtml = '<tr>'+ 
							'<td>秒</td>'+
							'<td>' + checkValue(dataList["jobs_detail"]["sched"]["seconds"]) + '</td>'+
							'</tr>' +
							'<tr>'+ 
								'<td>分</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["minutes"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>小时</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["hours"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>周</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["weeks"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["days"]) + '</td>'+
							'</tr>' +
							'<tr>'+ 
								'<td>开始日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["start_date"]) + '</td>'+
							'</tr>' +	
							'<tr>'+ 
								'<td>结束日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["end_date"]) + '</td>'+
							'</tr>' 			
		}else{
			var schedHtml = '<tr>'+ 
								'<td>运行日期</td>'+
								'<td>' + checkValue(dataList["jobs_detail"]["sched"]["run_date"]) + '</td>'+
							'</tr>' 		
		}		
	}
	var vHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
					'<legend>调度信息</legend>' +
						'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
						     schedHtml +
						'</table>'
				'</div>'; 				
	return '<div class="row">'+ vHtml + '</div>' + nHtml + '</div>';	
}	

function AssetsSelect(name,dataList,selectIds){
	
	if(!selectIds){selectIds=0}
	
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		var text = dataList[i]["detail"]["ip"]+ ' | ' + dataList[i]["project"]+' | '+dataList[i]["service"]				
		if(selectIds==dataList[i]["id"]){
			selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
		}else{
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		} 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}


function SchedNodeSelect(name,dataList,selectIds){
	
	if(!selectIds){selectIds=0}
	
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		var text = dataList[i]["ip"]+ ' | ' + dataList[i]["port"]			
		if(selectIds==dataList[i]["sched_node"]){
			selectHtml += '<option selected="selected" value="'+ dataList[i]["sched_node"] +'">'+text +'</option>' 	
		}else{
			selectHtml += '<option value="'+ dataList[i]["sched_node"] +'">'+text +'</option>'
		} 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}


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

function InitDataTable(tableId,dataList,buttons,columns,columnDefs){
//	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	dataList,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 20,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
		$('input[name="node_enable"]').bootstrapSwitch({  
	        onText:"上线",  
	        offText:"下线",  
	        onColor:"success",  
	        offColor:"danger",  
	        size:"mini",
	        onSwitchChange:function(event,state){  
	            if(state==true){  
	               console.log('已打开');  
	            }else{  
	            	console.log('已关闭');  
	            }  
	            console.log(this.value)
	            if(state==true){  
	                var data = {
	            			"sched_node":this.value,
	            			"enable":1
	            		} 
	            }else{  
	                var data = {
	            			"sched_node":this.value,
	            			"enable":0
	            		}  
	            }  
	            console.log(data)
	            updateJobsStatus('/sched/apsched/node/',data)            
	        }  
	    }) 
	}

function RefreshTable(tableId, urlData){
	  $.getJSON(urlData, null, function( dataList )
	  {
	    table = $(tableId).dataTable();
	    oSettings = table.fnSettings();
	    
	    table.fnClearTable(this);

	    for (var i=0; i<dataList.length; i++)
	    {
	      table.oApi._fnAddData(oSettings, dataList[i]);
	    }

	    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	    table.fnDraw();
		$('input[name="node_enable"]').bootstrapSwitch({  
	        onText:"上线",  
	        offText:"下线",  
	        onColor:"success",  
	        offColor:"danger",  
	        size:"mini",
	        onSwitchChange:function(event,state){  
	            if(state==true){  
	               console.log('已打开');  
	            }else{  
	            	console.log('已关闭');  
	            }  
	            console.log(this.value)
	            if(state==true){  
	                var data = {
	            			"sched_node":this.value,
	            			"enable":1
	            		} 
	            }else{  
	                var data = {
	            			"sched_node":this.value,
	            			"enable":0
	            		}  
	            }  
	            updateJobsStatus('/sched/apsched/node/',data)            
	        }  
	    }) 	      
	  });
	}

function AutoReload(tableId,url){
	  RefreshTable('#'+tableId, url);
	  setTimeout(function(){AutoReload(url);}, 30000);
}

	
function InitJobsDataTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Bfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	data['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 20,
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
	  
	$('input[name="is_alert"]').bootstrapSwitch({  
        onText:"开启",  
        offText:"关闭",  
        onColor:"success",  
        offColor:"info",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
                var data = {
            			"id":this.value,
            			"is_alert":1
            		} 
            }else{  
                var data = {
            			"id":this.value,
            			"is_alert":0
            		}  
            }  
            updateJobsStatus('/sched/apsched/node/jobs/',data)
        }  
    }) 
    
	$('input[name="jobs_status"]').bootstrapSwitch({  
        onText:"运行",  
        offText:"关闭",  
        onColor:"success",  
        offColor:"danger",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
               var data = {
            			"id":this.value,
            			"status":"running"
            		}
            }
            else{  
                var data = {
            			"id":this.value,
            			"status":"remove"
                	}
            }    
            updateJobsStatus('/sched/apsched/node/jobs/',data)
        }  
    }) 	  
	  
}

function InitJobsLogsDataTable(tableId,url,buttons,columns,columnDefs){
	  jobsDataList = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Bfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	jobsDataList['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"iDisplayLength": 20,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (jobsDataList['next']){
		  $("button[name='log_page_next']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='log_page_next']").attr("disabled", true).val();
	  }
	  if (jobsDataList['previous']){
		  $("button[name='log_page_previous']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='log_page_previous']").attr("disabled", true).val();
	  }	   
}

function updateJobsStatus(urls,data){
	$.ajax({  
        type: "PUT",  
        url:urls, 
        dataType: "json",
		data:data,					
        error: function(response) {  
        	new PNotify({
                title: 'Ops Failed!',
                text: response.responseText,
                type: 'error',
                styling: 'bootstrap3'
            });       
        },  
        success: function(response) {  
			if (response["code"] == "200"){
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
			RefreshJobsTable('schedNodeJobsManageListTable', '/api/sched/apsched/jobs/')
        }  
	});	
}

function RefreshJobsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList['results'].length; i++)
    {
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
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
    
	$('input[name="is_alert"]').bootstrapSwitch({  
        onText:"开启",  
        offText:"关闭",  
        onColor:"success",  
        offColor:"info",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
                var data = {
            			"id":this.value,
            			"is_alert":1
            		} 
            }else{  
                var data = {
            			"id":this.value,
            			"is_alert":0
            		}  
            }  
            updateJobsStatus('/sched/apsched/node/jobs/',data)
        }  
    }) 
    
	$('input[name="jobs_status"]').bootstrapSwitch({  
        onText:"运行",  
        offText:"关闭",  
        onColor:"success",  
        offColor:"danger",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
               var data = {
            			"id":this.value,
            			"status":"running"
            		}
            }
            else{  
                var data = {
            			"id":this.value,
            			"status":"remove"
                	}
            }    
            updateJobsStatus('/sched/apsched/node/jobs/',data)
        }  
    }) 	  
    
  });	
}

function RefreshJobsLogsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){

    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);
 
    for (var i=0; i<dataList['results'].length; i++){
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
      jobsResults[dataList["results"][i]["id"]] = dataList["results"][i]["result"]
    }
    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='log_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='log_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='log_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='log_page_previous']").attr("disabled", true).val();
    }  
    
  });	
}
	
function makeSchedNodeManageTableList(dataList){
    var columns = [
                   {"data": "sched_node"},
                   {"data": "ip"},
                   {"data": "port"},                  
	               {"data": "token"},
	               {"data": "jobs_count"},
	               {"data": "enable"},
	               ]
   var columnDefs = [
	    		        {
	   	    				targets: [4],
	   	    				render: function(data, type, row, meta) {  
	   	                        return '<span class="badge badge-primary">'+ row.jobs_count +'</span>'
	   	    				},
	   	    				"className": "text-center",
		    		    },                      
	    		        {
	   	    				targets: [5],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.enable==1){
	   	    						return '<input class="switch switch-mini" name="node_enable" type="checkbox" data-size="mini"  value="'+ row.sched_node + '" checked />'
	   	    					}else{
	   	    						return '<input class="switch switch-mini" name="node_enable" type="checkbox" data-size="mini"  value="'+ row.sched_node + '"/>'
	   	    					}
	   	    				}
	    		        },      		        
	    		        {
   	    				targets: [6],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-node-edit" value="'+ row.sched_node +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +  
	    	                           '<button type="button" name="btn-node-add" value="'+ row.sched_node +'" class="btn btn-default"><span class="fa fa-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' +	    	                               	                           
	    	                           '<button type="button" name="btn-node-delete" value="'+ row.sched_node +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
        	$('#myAddUserModal').modal("show")
        }
    }]    
	InitDataTable('schedNodeManageListTable',dataList,buttons,columns,columnDefs);	
}	

function makeschedNodeJobsManageTableList(){
    var columns = [
		           {
		                "className": 'details-control',
		                "orderable": false,
		                "data":      null,
		                "defaultContent": ''
		           },                   
                   {"data": "id"},
                   {"data": "node_detail.sched_server"},
                   {"data": "job_name"},
                   {"data": "jobs_detail.cmd"},
                   {"data": "runs"},
                   {"data": "jobs_detail.type"},
                   {"data": "jobs_detail.id"},
                   {"data": "jobs_detail.status"},
                   {"data": "alert_detail.is_alert"},
	               ]
   var columnDefs = [  
	    		        {
	   	    				targets: [5],
	   	    				render: function(data, type, row, meta) {  
	   	                        return '<span class="badge badge-primary">'+ row.runs +'</span>'
	   	    				},
	   	    				"className": "text-center",
		    		    },                      
	    		        {
	   	    				targets: [6],
	   	    				render: function(data, type, row, meta) {  
	   	                        return "<code>"+sched_type_array[row.jobs_detail.type]+"<code>"
	   	    				},
	   	    				"className": "text-center",
		    		    },                      
	    		        {
	   	    				targets: [8],
	   	    				render: function(data, type, row, meta) {  
	   	    					if (row.jobs_detail.status=="running"){
	   	    						var status = '<input class="switch switch-mini" name="jobs_status" type="checkbox" data-size="mini"  value="'+ row.id + '" checked />'
	   	    					}else{
	   	    						var status = '<input class="switch switch-mini" name="jobs_status" type="checkbox" data-size="mini"  value="'+ row.id + '"/>'
	   	    					}
	   	                        return status
	   	    				},
	   	    				"className": "text-center",
		    		    },                      
	    		        {
	   	    				targets: [9],
	   	    				render: function(data, type, row, meta) {  
	   	    					if (row.alert_detail.is_alert==1){
	   	    						var check = '<input class="switch switch-mini" name="is_alert" type="checkbox" data-size="mini"  value="'+ row.id + '" checked />'
	   	    					}else{
	   	    						var check = '<input class="switch switch-mini" name="is_alert" type="checkbox" data-size="mini"  value="'+ row.id + '"/>'
	   	    					}
	   	                        return check
	   	    				},
	   	    				"className": "text-center",
		    		    },                     
	    		        {
   	    				targets: [10],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-jobs-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                           '<button type="button" name="btn-jobs-notice" value="'+ row.id +'" class="btn btn-default" data-toggle="modal"><span class="fa fa-weixin" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-jobs-logs" value="'+ row.id +'" class="btn btn-default" data-toggle="modal"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-jobs-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = []    
    InitJobsDataTable('schedNodeJobsManageListTable','/api/sched/apsched/jobs/',buttons,columns,columnDefs);	
}


function makeschedNodeJobsLogsTableList(url){
    var columns = [                 
                   {"data": "id"},
                   {"data": "jobname"},
                   {"data": "cmd"},
                   {"data": "stime"},
                   {"data": "etime"},
                   {"data": "runtime"},
                   {"data": "result"},
                   {"data": "status"}
	               ]
   var columnDefs = [                      
                       {
							targets: [3],
							render: function(data, type, row, meta) {  	    					
					         return UnixToDate(row.stime)
							},
							"className": "text-center",
					   },                                            
                   	   {
							targets: [4],
							render: function(data, type, row, meta) {  	    					
				              return UnixToDate(row.etime)
							},
							"className": "text-center",
				        },  
	                   	{
							targets: [6],
							render: function(data, type, row, meta) {  
								if (row.result.length > 100){
									return '<button type="button" name="btn-jobs-logs-detail" data-toggle="modal" class="btn btn-link" value="'+ row.id +'">'+row.result.substring(-1,10)+'...</button>'
								}
								else{
									return '<button type="button" name="btn-jobs-logs-detail" data-toggle="modal" class="btn btn-link" value="'+ row.id +'">'+row.result+'</button>'
								}
				              
							},
							"className": "text-center",
				        }, 					        
	                   	{
							targets: [7],
							render: function(data, type, row, meta) {  	    	
								if (row.status==0){
									return '<span class="label label-success">成功</span>'
								}else{
									return '<span class="label label-danger">失败</span>'
								}
				              
							},
							"className": "text-center",
				        }, 			        
	    		        {
   	    				targets: [8],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +		    	                           
	    	                           '<button type="button" name="btn-jobs-logs-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = []    
    InitJobsLogsDataTable('schedNodeJobsLogsListTable',url,buttons,columns,columnDefs);	
}


function controlSchedSelectHide(value,selectIds){
	if(!selectIds){selectIds=0}
	switch(value)
	   {
		   case "cron":
			   $("#sched_type_cron").show();
			   $("#sched_type_common").show();
			   $("#sechd_date_range").show();
			   $("#sechd_date_run").hide();
		       break;
		   case "interval":
			   $("#sched_type_cron").hide();
			   $("#sched_type_common").show();
			   $("#sechd_date_range").show();
			   $("#sechd_date_run").hide();
		       break;
		   case "date":
			   $("#sched_type_cron").hide();
			   $("#sched_type_common").hide();
			   $("#sechd_date_range").hide();
			   $("#sechd_date_run").show();			 
		       break;		   		   
		   default:
			   $("#sched_type_cron").show();
		   	   $("#sched_type_common").show();
			   $("#sechd_date_range").show();		   	   
		       $("#sechd_date_run").hide();
	   }
	sched_type = value
}

var sched_type="cron"

$(document).ready(function() {	
	
	
	if($("#sched_server").length){
		var dataList = requests('get','/api/assets/?assets_type=ser')
		AssetsSelect("sched_server",dataList)
	}	

	
	$("#sched_type").change(function(){
		   var obj = document.getElementById("sched_type"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   controlSchedSelectHide(value);	
	});	

	if($("#sched_node_job").length){
		var dataList = requests('get','/api/sched/apsched/node/')
		SchedNodeSelect("sched_node_job",dataList) 
		makeSchedNodeManageTableList(dataList)
		$("#sched_node_job").change(function(){
			   var obj = document.getElementById("sched_node_job"); 
			   var index = obj.selectedIndex;
			   var value = obj.options[index].value; 
			   RefreshJobsTable('schedNodeJobsManageListTable','/api/sched/apsched/jobs/?job_node='+value)
		});			
	}		
	
	if($("input[name$='date']").length){
		$("input[name$='date']").datetimepicker({
			format: 'yyyy-mm-dd hh:ii:ss',
	        pickDate: true,
	        pickTime: true,
	        hourStep: 1,
	        minuteStep: 5,
	        secondStep: 30,
		});		
	}
	
	if($("#schedNodeJobsManageListTable").length){

	    $("button[name^='page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshJobsTable('schedNodeJobsManageListTable', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	    makeschedNodeJobsManageTableList()  
	}
		
  
    $('#schedNodeJobsManageListTable tbody').on('click', 'td.details-control', function () {
    	var table = $('#schedNodeJobsManageListTable').DataTable();
    	var dataList = [];
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        aId = row.data()["id"];
        $.ajax({
            url : "/api/sched/apsched/jobs/?id="+aId,
            type : "get",
            async : false,
            success : function(result) {             
            	try {
            		dataList = result.results[0];
            		}
        		catch(error) {
        			dataList = {};
        		  console.error(error);
        		}            	
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
  
    
	$('#schedNodeManageListTable tbody').on('click',"button[name='btn-node-edit']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var node =  td.eq(1).text()
    	var port =  td.eq(2).text()
    	var token =  td.eq(3).text()
    	var enable =  td.eq(4).text()
    	if(enable=="上线"){
    		var isActiveSelect = '<select class="form-control" name="modf_enable"><option selected="selected" name="modf_enable" value="1">上线</option><option name="modf_enable" value="0">下线</option></select>'
    	}else{
    		var isActiveSelect = '<select class="form-control" name="modf_enable"><option name="modf_enable" value="0">下线</option><option selected="selected" name="modf_enable" value="1">上线</option></select>'
    	}    	
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ node +'</strong>节点配置',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">端口<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="modf_port" value="'+ port +'"  required="required"  class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">Token<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              	'<textarea row="3" class="form-control" name="modf_token"  required="required"  class="form-control col-md-7 col-xs-12">'+ token +'</textarea>' +
			              '</div>' +
			            '</div>' + 	
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">激活<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              		isActiveSelect +
			              '</div>' +
			            '</div>' + 			            
			          '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var port = this.$content.find("[name='modf_port']").val();
	                    var token = this.$content.find("[name='modf_token']").val()
	                    var enable = this.$content.find("select[name='modf_enable'] option:selected").val()
				    	$.ajax({  
				            type: "PUT",  
				            url:"/sched/apsched/node/",  
							data:{
								"sched_node":vIds,
				            	"token":token,
				            	"port":port,
				            	"enable":enable,
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
					                    text: '删除成功',
					                    type: 'success',
					                    styling: 'bootstrap3'
					                }); 
					            	RefreshTable('#schedNodeManageListTable', '/api/sched/apsched/node/')
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
	                }
	            }
	        }
	    });
    });	
	
	$('#schedNodeManageListTable tbody').on('click',"button[name='btn-node-add']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var node =  td.eq(1).text()
    	var port =  td.eq(2).text()
		var dataList = requests('get','/api/sched/apsched/node/')
		SchedNodeSelect("sched_node",dataList,vIds)    	
    	$("#add_sched_node_task").show()
    	$("#sched_instructions").show();
    	$("#sched_jobs_log").hide();
    	$("#add_sched_jobs").val(vIds)
	})
    
	$('#schedNodeManageListTable tbody').on('click',"button[name='btn-node-delete']",function(){
		var vIds = $(this).val();  
    	var td = $(this).parent().parent().parent().find("td")
    	var node =  td.eq(1).text()
    	var port =  td.eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>节点</strong> <code>' + node + ':' + port + '</code>?',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:"/sched/apsched/node/", 
					type:"DELETE",  		
					data:{
						"sched_node":vIds,
					}, 
					success:function(response){
		            	if (response["code"] == 200){
			            	new PNotify({
			                    title: 'Success!',
			                    text: '修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('#schedNodeManageListTable', '/api/sched/apsched/node/')
		            	}else{
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: response["msg"],
			                    type: 'error',
			                    styling: 'bootstrap3'
			                });  				            		
		            	}
					},
			    	error:function(response){
			           	new PNotify({
			                   title: 'Ops Failed!',
			                   text: response.responseText,
			                   type: 'error',
			                   styling: 'bootstrap3'
			               }); 
			    	}
				});	
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});			  		 	
    });		

    $("#addNodesubmit").on('click', function() {
    	var form = document.getElementById('addNodeForm');
    	var post_data = {};
    	for (var i = 1; i < form.length; ++i) {
    		var name = form[i].name;
    		var value = form[i].value;
    		if (value.length==0 && name.length > 0){
    			console.log(name)
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 
    			return false;
    		}else if(name.length > 0 && value.length > 0){
    			post_data[name] = value
    		}
    	};
    	$.ajax({  
            type: "POST",             
            url:"/sched/apsched/node/",  
            data:post_data,
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
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
	            	RefreshTable('#schedNodeManageListTable', '/api/sched/apsched/node/')
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
    });		
		
    $('#add_sched_jobs').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);
		var formData = new FormData();	
		var jobsForm = document.getElementById('addSchedJobsForm');
		for (var i = 0; i < jobsForm.length; ++i) {
			var name = jobsForm[i].name;
			var value = jobsForm[i].value;					
			if (name.length >0 && value.length > 0 && name !== "csrfmiddlewaretoken"){
				formData.append(name,value);	
			};					
		};	
		var noticeForm = document.getElementById('addSchedJobsNoticeForm')
		for (var j = 0; j < noticeForm.length; ++j) {
			var name = noticeForm[j].name;
			var value = noticeForm[j].value;					
			if (name.length >0 && value.length > 0 && name !== "csrfmiddlewaretoken"){
				formData.append(name,value);	
			};					
		};	
		$.ajax({
			url:'/sched/apsched/node/jobs/', //请求地址
			type:"POST",  //提交类似	
		    processData: false,
		    contentType: false,				
			data:formData, 			
			success:function(response){
				btnObj.removeAttr('disabled');
				if (response["code"] == "200"){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
	            	RefreshJobsTable('schedNodeJobsManageListTable', '/api/sched/apsched/jobs/')
				}else{
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response["msg"],
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 					
				}
				
				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });    
    
    
	$('#schedNodeJobsManageListTable tbody').on('click',"button[name='btn-jobs-edit']",function(){
    	var vIds = $(this).val();
    	try {
    		  var data = requests('get',"/api/sched/apsched/jobs/?id="+vIds)["results"][0]
    		}
		catch(error) {
		  console.error(error);
		  return false
		}

		if(data["jobs_detail"]["type"]=="cron"){
			var contentHtml = '<form role="form" name="modfSchedJobsForm" data-parsley-validate class="form-horizontal form-label-left">' +
							'<fieldset>' +	
				            '<div class="item form-group">' +
				                '<label class="col-sm-2 control-label">'+'<font color="red">*</font>任务名称</label>'+
				                '<div class="col-sm-8">'+
				                 '<input class="form-control" name="job_name" value="'+ data["job_name"] +'" required>'+
				                '</div>'+
				            '</div>'+  																																																																																													
							
							'<div id="sched_type_common">'+
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">秒</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="second" name="second"  value="'+ checkValue(data["jobs_detail"]["sched"]["second"]) +'"  class="input-xlarge" title="正确格式：00-59 or * or */1"  required/>' +
									 '</div>'+
								'</div>'+						
								
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">分</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="minute" name="minute"  value="'+ checkValue(data["jobs_detail"]["sched"]["minute"]) +'"  class="input-xlarge" required  title="正确格式：00-59 or * or */1"  required/>'+
									 '</div>'+
								'</div>'+
								
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">时</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="hour" name="hour"  value="'+ checkValue(data["jobs_detail"]["sched"]["hour"]) +'" class="input-xlarge" required   title="小时" required/>'+
									 '</div>'+
								'</div>'+	
				
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">日</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="day" name="day"  value="'+ checkValue(data["jobs_detail"]["sched"]["day"]) +'" class="input-xlarge"  title="日期" required/>'+
									 '</div>'+
								'</div>'+	
								
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">周</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="week" name="week"  value="'+ checkValue(data["jobs_detail"]["sched"]["week"]) +'" title="" class="input-xlarge" required/>'+
									 '</div>'+
								'</div>'+									
								
						   '</div>'+	
						   '<div id="sched_type_cron">'+
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">月</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="month" name="month"  value="'+ checkValue(data["jobs_detail"]["sched"]["month"]) +'"  class="input-xlarge"  title="月份" required/>'+
									 '</div>'+
								'</div>'+															
											
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">星期</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="day_of_week" name="day_of_week"  value="'+ checkValue(data["jobs_detail"]["sched"]["day_of_week"]) +'" class="input-xlarge"  required/>'+
									 '</div>'+
								'</div>'+	
								
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">年</label>'+
									 '<div class="col-sm-8">'+
									 	'<input type="text" class="form-control" id="year" name="year" placeholder="2019" value="'+ checkValue(data["jobs_detail"]["sched"]["year"]) +'" class="input-xlarge"/>'+
									 '</div>'+
								'</div>'+									
							'</div>'+
				
							'<div id="sechd_date_range">'+
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">开始日期</label>'+
				                   '<div class="col-md-8 col-xs-12 xdisplay_inputx form-group has-feedback">'+
				                     '<input type="text" class="form-control has-feedback-left" name="start_date" id="start_date"  value="'+ checkValue(data["jobs_detail"]["sched"]["start_date"]) +'" required>'+
				                     '<span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true"></span>'+
				                   '</div>'+	
								'</div>'+	
				
								'<div class="item form-group">'+
									 '<label class="col-sm-2 control-label">结束日期</label>'+
				                   '<div class="col-md-8 col-xs-12 xdisplay_inputx form-group has-feedback">'+
				                     '<input type="text" class="form-control has-feedback-left" name="end_date" id="end_date"  value="'+ checkValue(data["jobs_detail"]["sched"]["end_date"]) +'" required>'+
				                     '<span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true">'+'</span>'+
				                   '</div>'+	
								'</div>'+																			
							'</div>'+		
				
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label"><font color="red"></font>命令</label>'+
								 '<div class="col-sm-8">'+
								 	'<textarea type="text" row="5" class="form-control" id="job_command" name="job_command" placeholder="/usr/sbin/ntpdate time.windows.com" class="input-xlarge">'+ checkValue(data["jobs_detail"]["cmd"]) +'</textarea>'+
								 '</div>'+
							'</div>'+																													
							'</fieldset>'+									 		
						'</form>'
		}else if (data["jobs_detail"]["type"]=="interval"){
			var contentHtml = '<form role="form" name="modfSchedJobsForm" data-parsley-validate class="form-horizontal form-label-left">' +
						'<fieldset>' +	
			            '<div class="item form-group">' +
			                '<label class="col-sm-2 control-label">'+'<font color="red">*</font>任务名称</label>'+
			                '<div class="col-sm-8">'+
			                 '<input class="form-control" name="job_name" id="job_name" value="'+ data["job_name"] +'" required>'+
			                '</div>'+
			            '</div>'+  																																																																																														
						
						'<div id="sched_type_common">'+
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">秒</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text" class="form-control" id="second" name="second"  value="'+ checkValue(data["jobs_detail"]["sched"]["seconds"]) +'"  class="input-xlarge" title="正确格式：00-59 or * or */1"  required/>' +
								 '</div>'+
							'</div>'+						
							
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">分</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text" class="form-control" id="minute" name="minute"  value="'+ checkValue(data["jobs_detail"]["sched"]["minutes"]) +'"  class="input-xlarge" required  title="正确格式：00-59 or * or */1"  required/>'+
								 '</div>'+
							'</div>'+
							
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">时</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text" class="form-control" id="hour" name="hour"  value="'+ checkValue(data["jobs_detail"]["sched"]["hours"]) +'" class="input-xlarge" required   title="小时" required/>'+
								 '</div>'+
							'</div>'+	
			
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">日</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text" class="form-control" id="day" name="day"  value="'+ checkValue(data["jobs_detail"]["sched"]["days"]) +'" class="input-xlarge"  title="日期" required/>'+
								 '</div>'+
							'</div>'+	
							
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">周</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text" class="form-control" id="week" name="week"  value="'+ checkValue(data["jobs_detail"]["sched"]["weeks"]) +'" title="" class="input-xlarge" required/>'+
								 '</div>'+
							'</div>'+									
							
					    '</div>'+	
			
						'<div id="sechd_date_range" >'+
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">开始日期</label>'+
			                   '<div class="col-md-8 col-xs-12 xdisplay_inputx form-group has-feedback">'+
			                     '<input type="text" class="form-control has-feedback-left" name="start_date" id="start_date"  value="'+ checkValue(data["jobs_detail"]["sched"]["start_date"]) +'" required>'+
			                     '<span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true"></span>'+
			                   '</div>'+	
							'</div>'+	
			
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">结束日期</label>'+
			                   '<div class="col-md-8 col-xs-12 xdisplay_inputx form-group has-feedback">'+
			                     '<input type="text" class="form-control has-feedback-left" name="end_date" id="end_date"  value="'+ checkValue(data["jobs_detail"]["sched"]["end_date"]) +'" required>'+
			                     '<span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true">'+'</span>'+
			                   '</div>'+	
							'</div>'+																			
						'</div>'+		
			
						'<div class="item form-group">'+
							 '<label class="col-sm-2 control-label"><font color="red"></font>命令</label>'+
							 '<div class="col-sm-8">'+
							 	'<textarea type="text" row="5" class="form-control" id="job_command" name="job_command" placeholder="/usr/sbin/ntpdate time.windows.com"  class="input-xlarge">'+ checkValue(data["jobs_detail"]["cmd"]) + '</textarea>'+
							 '</div>'+
						'</div>'+																													
						'</fieldset>'+									 		
					'</form>'		
		}else{
			var contentHtml = '<form role="form" name="modfSchedJobsForm" data-parsley-validate class="form-horizontal form-label-left">' +
					'<fieldset>' +	
		            '<div class="item form-group">' +
		                '<label class="col-sm-2 control-label">'+'<font color="red">*</font>任务名称</label>'+
		                '<div class="col-sm-8">'+
		                 '<input class="form-control" name="job_name" id="job_name" value="'+ data["job_name"] +'" required>'+
		                '</div>'+
		            '</div>'+  											
																																																																												
					'<div id="sechd_date_run">'+
						'<div class="item form-group">'+
							 '<label class="col-sm-2 control-label"><font color="red"></font>日期</label>'+
		                   '<div class="col-md-8 col-xs-12 xdisplay_inputx form-group has-feedback">'+
		                     '<input type="text" class="form-control has-feedback-left" name="run_date" id="run_date"  value="'+ checkValue(data["jobs_detail"]["sched"]["run_date"]) +'" required>'+
		                     '<span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true"></span>'+
		                   '</div>'+	
						'</div>'+								
					'</div>'+							
					
					'<div class="item form-group">'+
						 '<label class="col-sm-2 control-label"><font color="red"></font>命令</label>'+
						 '<div class="col-sm-8">'+
						 	'<textarea type="text" row="5" class="form-control" id="job_command" name="job_command" placeholder="/usr/sbin/ntpdate time.windows.com" class="input-xlarge">' + checkValue(data["jobs_detail"]["cmd"]) + '</textarea>'+
						 '</div>'+
					'</div>'+																													
					'</fieldset>'+									 		
				'</form>'			
		}
    	var td = $(this).parent().parent().parent().find("td")
    	var jobsName =  td.eq(3).text() 
    	var jobsType = td.eq(5).text() 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ jobsName +'</strong>任务-<code>'+jobsType+'</code>',
	        content: contentHtml,
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	                	console.log(this.$content)
	            		var jobsForm = this.$content.find('input,textarea');                	
	            		for (var i = 0; i < jobsForm.length; ++i) {
	            			var name =  jobsForm[i].name
	            			var value = jobsForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
	            		formData["id"] = vIds;
				    	$.ajax({  
				            type: "PUT",  
				            url:"/sched/apsched/node/jobs/", 
				            dataType: "json",
							data:formData,					
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });       
				            },  
				            success: function(response) {  
								if (response["code"] == "200"){
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
								RefreshJobsTable('schedNodeJobsManageListTable', '/api/sched/apsched/jobs/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#schedNodeJobsManageListTable tbody').on('click',"button[name='btn-jobs-notice']",function(){
    	var vIds = $(this).val();
    	try {
    		  var data = requests('get',"/api/sched/apsched/jobs/?id="+vIds)["results"][0]
    		}
		catch(error) {
		  console.error(error);
		  return false
		}
        if(data["alert_detail"]["is_alert"]==1){
        	var is_alert = '<option value="0">关闭</option><option  selected="selected"  value="1">开启</option>'
        }
        else{
        	var is_alert = '<option selected="selected" value="0">关闭</option><option value="1">开启</option>'
        }
        if (data["alert_detail"]["notice_trigger"]==0){
        	var notice_trigger = '<option selected="selected"  value="0">失败</option><option  value="1">成功</option><option  value="2">完成</option>'
        }
        else if(data["alert_detail"]["notice_trigger"]==1){
        	var notice_trigger = '<option value="0">失败</option><option selected="selected" value="1">成功</option><option  value="2">完成</option>'
        }
        else{
        	var notice_trigger = '<option value="0">失败</option><option  value="1">成功</option><option selected="selected" value="2">完成</option>'
        }
        if(data["alert_detail"]["notice_type"]==0){
        	var notice_type = '<option selected="selected"  value="0">邮件</option><option  value="1">微信</option><option  value="2">钉钉</option>'
        }
        else if (data["alert_detail"]["notice_type"]==1){
        	var notice_type = '<option value="0">邮件</option><option selected="selected" value="1">微信</option><option value="2">钉钉</option>'
        }
        else{
        	var notice_type = '<option value="0">邮件</option><option value="1">微信</option><option selected="selected" value="2">钉钉</option>'
        }        
		var contentHtml = '<form role="form" name="modfSchedJobsNoticeForm" data-parsley-validate class="form-horizontal form-label-left">' +
							'<div class="item form-group">' +
								 '<label class="col-sm-2 control-label">激活</label>' +
								 '<div class="col-sm-8">' +
	                                 '<select required="required" class="form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control" id="is_alert" name="is_alert"   required>' +
	                                      is_alert +                        	
	                                 '</select>' +
								 '</div>' +
							'</div>' +
							'<div class="item form-group">' +
								 '<label class="col-sm-2 control-label">触发类型</label>' +
								 '<div class="col-sm-8">' +
	                                 '<select required="required" class="form-control"  data-size="10" data-selected-text-format="count > + 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control" id="notice_trigger" name="notice_trigger"   required>' +
	                                      notice_trigger +                           	
	                                 '</select>' +
								 '</div>' +
							'</div>' +								
							'<div class="item form-group">' +
								 '<label class="col-sm-2 control-label">通知类型</label>' +
								 '<div class="col-sm-8">' +
	                                 '<select required="required" class="form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control" id="notice_type" name="notice_type"   required>' +
										'<option selected="selected"  value="0">邮件</option>' +
											notice_type +
	                                 '</select>' +
								 '</div>' +
							'</div>' +															
							'<div class="item form-group">' +
								 '<label class="col-sm-2 control-label">通知对象</label>' +
								 '<div class="col-sm-8">' +
								 	'<textarea type="text" row="5" class="form-control" id="notice_number" name="notice_number" placeholder="多个对象以;号隔开" value="" class="input-xlarge">'+ checkValue(data["alert_detail"]["notice_number"]) +'</textarea>' +
								 '</div>' +
							'</div>' +								
							'<div class="item form-group">' +
								 '<label class="col-sm-2 control-label">间隔</label>' +
								 '<div class="col-sm-8">' +
	                                 '<input type="text" class="form-control" id="notice_interval" name="notice_interval" placeholder="多少秒内重复失败不会通知" value="'+ checkValue(data["alert_detail"]["notice_interval"]) +'" class="input-xlarge"/>' +
								 '</div>' +
							'</div>' +
						'</form>'		

    	var td = $(this).parent().parent().parent().find("td")
    	var jobsName =  td.eq(3).text() 
    	var jobsType = td.eq(5).text() 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>' + jobsName +'</strong>任务-通知类型',
	        content: contentHtml,
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	                	console.log(this.$content)
	            		var jobsForm = this.$content.find('input,textarea,select');                	
	            		for (var i = 0; i < jobsForm.length; ++i) {
	            			var name =  jobsForm[i].name
	            			var value = jobsForm[i].value 
	            			if (name.length > 0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
	            		formData["id"] = vIds;
				    	$.ajax({  
				            type: "PUT",  
				            url:"/sched/apsched/node/jobs/", 
				            dataType: "json",
							data:formData,					
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });       
				            },  
				            success: function(response) {  
								if (response["code"] == "200"){
					            	new PNotify({
					                    title: 'Success!',
					                    text: '添加成功',
					                    type: 'success',
					                    styling: 'bootstrap3'
					                }); 
					            	RefreshJobsTable('schedNodeJobsManageListTable', '/api/sched/apsched/jobs/')
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
	                }
	            }
	        }
	    });
    });	
    
	$('#schedNodeJobsManageListTable tbody').on('click',"button[name='btn-jobs-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(3).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>任务</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/sched/apsched/node/jobs/", 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
						if (response["code"] == "200"){
			            	new PNotify({
			                    title: 'Success!',
			                    text: '删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshJobsTable('schedNodeJobsManageListTable', '/api/sched/apsched/jobs/')
						}else{
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: response["msg"],
			                    type: 'error',
			                    styling: 'bootstrap3'
			                }); 					
						}												
					},
			    	error:function(response){
			           	new PNotify({
			                   title: 'Ops Failed!',
			                   text: response.responseText,
			                   type: 'error',
			                   styling: 'bootstrap3'
			               }); 
			    	}
				});	
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});			  		 	
    });	  
	
	$('#schedNodeJobsManageListTable tbody').on('click',"button[name='btn-jobs-logs']",function(){
		var vIds = $(this).val();  
		var node =  $(this).parent().parent().parent().find("td").eq(2).text()
    	$("#add_sched_node_task").hide()
    	$("#sched_instructions").hide();
		$("#sched_jobs_log").show();
		$("#jobs_nodes_name").html(node)
        if ($('#schedNodeJobsLogsListTable').hasClass('dataTable')) {
            dttable = $('#schedNodeJobsLogsListTable').dataTable();
            dttable.fnClearTable(); //清空table
            dttable.fnDestroy(); //还原初始化datatable
        }		
		makeschedNodeJobsLogsTableList('/api/sched/apsched/logs/?id='+vIds)		
		if(jobsDataList["results"].length){
			for (var i = 0; i < jobsDataList["results"].length; ++i) {
				jobsResults[jobsDataList["results"][i]["id"]] = jobsDataList["results"][i]["result"]
			}
		}
		
    });		
	
	if($("#schedNodeJobsLogsListTable").length){

	    $("button[name^='log_page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshJobsLogsTable('schedNodeJobsLogsListTable', url);      		
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 	 
	    
	    $('#schedNodeJobsLogsListTable tbody').on('click', 'button[name="btn-jobs-logs-detail"]', function () {
	    	var id = $(this).val()
	    	console.log(id)
	    	console.log(jobsResults)
	        $(this).pt({
	            position: 't', // 默认属性值
	            align: 'c',	   // 默认属性值
	            height: 'auto',
	            width: 'auto',
	            content: "<pre>"+jobsResults[id]+"</pre>"
	        });         
	    });  	    
	    
	}	
	
	$(function() {
		var jobsCount = requests('get','/api/sched/apsched/count/')
		$("#allNodes").text(jobsCount["data"]["allNodes"])
		$("#allJobs").text(jobsCount["data"]["allJobs"])
		$("#jobsSucess").text(jobsCount["data"]["jobsSucess"])
		$("#jobsFalied").text(jobsCount["data"]["jobsFalied"])
	})		
	

	
})