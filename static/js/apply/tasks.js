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

function get_dict_default_value(exp){
	if (typeof(exp) == "undefined"){
	    return "未知"
	}
	else{
		return exp
	}
}

function format_task_result(data){
	if(data['apply_detail']["apply_payload"].length > 0){
		var apply_payload = JSON.stringify(JSON.parse(data['apply_detail']["apply_payload"]), null, "\t")
	}
	else{
		var apply_payload = '无'
	}
	var taskHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    				'<legend>任务信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				  '<tr>' +
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">任务id:</td>' + 
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data["task_id"] +'</td>' +
	    				  '</tr>' +
	    				  '<tr>' +
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">任务参数:</td>' + 
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12"><pre>'+ JSON.stringify(JSON.parse(data["payload"]), null, "\t") +'</pre></td>' +
	    				  '</tr>'+
	    				  '<tr>' +
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">错误日志:</td>' + 
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12"><pre>'+ data["error_msg"] +'</pre></td>' +
	    				  '</tr>' +	    				  	
	    				'</table>' +
					'</div>'; 	
		
    var applyHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    				'<legend>应用信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				  '<tr>' +
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">应用类型:</td>' + 
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">'+ data['apply_detail']["apply_type"] +'</td>' +
	    				  '</tr>' +
	    				  '<tr>' +
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12">应用参数:</td>' + 
	    				  	'<td class="col-md-1 col-sm-12 col-xs-12"><pre>'+ apply_payload +'</pre></td>' +
	    				  '</tr>' +	    				  
	    				'</table>' +
					'</div>'; 				
    return '<div class="row">'+ taskHtml + applyHtml +'</div>';
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





function InitTaskDataTable(tableId,url,buttons,columns,columnDefs){
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
		    		"order": [[ 1, "ase" ]],
		    		"autoWidth": false,
		    		"iDisplayLength": 10
		    	});
	  if (jobsDataList['next']){
		  $("button[name='tasks_page_next']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='tasks_page_next']").attr("disabled", true).val();
	  }
	  if (jobsDataList['previous']){
		  $("button[name='tasks_page_previous']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='tasks_page_previous']").attr("disabled", true).val();
	  }	   
}

function RefreshTasksLogsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){

    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);
 
    for (var i=0; i<dataList['results'].length; i++){
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
    }
    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='tasks_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='tasks_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='tasks_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='tasks_page_previous']").attr("disabled", true).val();
    }  
    
  });	
}
	
function makeTasksLogsTableList(){
    var columns = [
                   {
					"className": 'details-control',
					"orderable": false,
					"data":      null,
					"defaultContent": ''
                   },	    
                   {"data": "id"},
                   {"data": "apply_detail"},
                   {"data": "user_info"},
                   {"data": "create_time"},                  
	               {"data": "update_time"},
	               {"data": "task_per"},
	               {"data": "status"}
	               ]
   var columnDefs = [  
	    		        {
   	    				targets: [2],
   	    				render: function(data, type, row, meta) {  	
/*   	                        return row.apply_detail['apply_name'];*/
							return  '<a href="javascript:;" class="user-profile" data-toggle="dropdown" aria-expanded="false">' +
				                      		'<img src="/media/'+ row.apply_detail['apply_icon']  +'"  alt="">'+ row.apply_detail['apply_name'] + '</a>'	   	    						 	                        
   	    				}
	    		        },    
	    		        {
   	    				targets: [3],
   	    				render: function(data, type, row, meta) {  	    					
   	    					if(typeof row.user_info['avatar'] == "undefined" || row.user_info['avatar'] == null || row.user_info['avatar'] == ""){
   	    						return  '<a href="javascript:;" class="user-profile" data-toggle="dropdown" aria-expanded="false">' +
				                      		'<img src="/static/images/img.jpg"  alt="">'+ row.user_info['username'] + '</a>'
   	    					}
   	    					else{
   	    						return  '<a href="javascript:;" class="user-profile" data-toggle="dropdown" aria-expanded="false">' +
				                      		'<img src="/media/'+ row.user_info['avatar']  +'"  alt="">'+ row.user_info['username'] + '</a>'	   	    						
   	    					}
   	    				},
   	    				"className": "text-center"
	    		        },  
	    		        {
   	    				targets: [6],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="progress progress_sm">' +
	                              		'<div class="progress-bar bg-green" role="progressbar" data-transitiongoal="'+ row.task_per +'" style="width: '+ row.task_per +'%;" aria-valuenow="'+ row.task_per +'"></div>' +
	                            	'</div>' +
	                               '<small>'+ row.task_per +'% Complete</small>';
   	    				},
   	    				"className":"project_progress"
	    		        }, 	    		        
	    		        {
   	    				targets: [7],
   	    				render: function(data, type, row, meta) {  	   
							switch (row.status) {
							  case 'stop':
							    return '<button type="button" class="btn btn-warning btn-sm">'+ row.status +'</button>';
							  case 'running':
							    return '<button type="button" class="btn btn-info btn-sm">'+ row.status +'</button>';
							  case 'failed':
							    return '<button type="button" class="btn btn-danger btn-sm">'+ row.status +'</button>';
							  case 'finished':
							    return '<button type="button" class="btn btn-success btn-sm">'+ row.status +'</button>';
							  case 'ready':
							    return '<button type="button" class="btn btn-primary btn-sm">'+ row.status +'</button>';
							  default:
							    return '<button type="button" class="btn btn-secondary btn-sm">'+ row.status +'</button>';
							}   	    					
   	                        
   	    				},
   	    				"className": "text-center"
	    		        },   
	    		        {
   	    				targets: [8],
   	    				render: function(data, type, row, meta) {  
   	    					var tagHtml = '<button type="button" name="btn-task-tag" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-tags" aria-hidden="true"></span></button>'
   	    					var delHtml = '<button type="button" name="btn-task-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span></button>'
							switch (row.status) {
							  case 'stop':
							    var stopHtml = '<button type="button" name="btn-task-stop" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-stop" aria-hidden="true"></span></button>'
							    break;
							  case 'running':
							    var stopHtml = '<button type="button" name="btn-task-stop" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-stop" aria-hidden="true"></span></button>'
							    var delHtml = '<button type="button" name="btn-task-delete"class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-trash" aria-hidden="true"></span></button>'
							    break;
							  case 'failed':
							    var stopHtml = '<button type="button" name="btn-task-stop" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-stop" aria-hidden="true"></span></button>'
							    break;
							  case 'finished':
							    var stopHtml = '<button type="button" name="btn-task-stop" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-stop" aria-hidden="true"></span></button>'
							    var tagHtml = '<button type="button" name="btn-task-tag" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-tags" aria-hidden="true"></span></button>'
							    break;
							  case 'ready':
							    var stopHtml = '<button type="button" name="btn-task-stop" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-stop" aria-hidden="true"></span></button>'
							    break;
							  default:
							    var stopHtml = '<button type="button" name="btn-task-stop" class="btn btn-default" aria-label="Justify" disabled><span class="fa fa-stop" aria-hidden="true"></span></button>'  
							    break;
							}     	    					
   	                        return '<div class="btn-group  btn-group-sm">' +		    	                           
	    	                           '<button type="button" name="btn-task-view"  value="'+ row.id +'" class="btn btn-default" data-toggle="modal"><span name="toggle-sidebar" class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                          	 stopHtml +  	                           
	    	                             delHtml +
	    	                             tagHtml + 
	    	                           '</div>';
   	    				}
	    		        }
	    		      ]	
    var buttons = [
                   ]    
    InitTaskDataTable('apply_tasks_table_list','/api/apply/tasks/',buttons,columns,columnDefs);	
}	


if($("#apply_tasks_table_list").length){

    $("button[name^='tasks_page_']").on("click", function(){
      	var url = $(this).val();
      	$(this).attr("disabled",true);
      	if (url.length){
      		RefreshTasksLogsTable('apply_tasks_table_list', url);
      	}      	
    	$(this).attr('disabled',false);
      }); 			
    makeTasksLogsTableList()  
}	

function get_task_count(){
	let dataList = requests('get','/api/apply/tasks/count/')
    for (var i=0; i<dataList.length; i++){
    	$("#"+dataList[i]["name"]+'_count').text(dataList[i]["count"])
    }	
}

$(document).ready(function() {	
	
	get_task_count()
	
	$('#simplerSidebar').simplerSidebar({
		opener: "button[name^='btn-task-view']",
		sidebar: {
		  align: 'right',
		  width: 800,
		  closingLinks: 'a'
		  }		
	});		
	
	$('#apply_tasks_table_list tbody').on('click',"button[name='btn-task-stop']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '终止确认',
		    content: '确认终止当前部署【'+ name +'】任务?',
		    type: 'red',
		    buttons: {
		        终止: function () {		       
				$.ajax({
					url:"/api/apply/task/"+ vIds + "/", 
					type:"PUT",  		
					success:function(response){
						RefreshTasksLogsTable('apply_tasks_table_list', '/api/apply/tasks/')											
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
		        }			        
		    }
		});			  		 	
    });		
	   
    		
	$('#apply_tasks_table_list tbody').on('click',"button[name='btn-task-view']",function(){
		var vIds = $(this).val();  
		var task_name = $(this).parent().parent().parent().find("td").eq(2).text()	
		var user_name = $(this).parent().parent().parent().find("td").eq(3).text()	
		let data = requests('get','/api/apply/task/detail/'+ vIds + '/')
		$("#apply_task_view_h2").html('<h2 id="apply_task_view_h2"><i class="fa fa-spinner"></i> '+ task_name +'应用任务运行日志 <small>Apply Run Task Log</small></h2>')
		var stats_li_strs = ''
		var err_li_strs = ''
		var lastest_li_strs = ''
	    for (var i=0; i<data['error_msg'].length; i++){
			var err_li_str = '<li>' +
		                      '<div class="block">' +
		                        '<div class="tags">' +
		                          '<a href="" class="tag">' +
		                            '<span>错误信息</span>' +
		                          '</a>' +
		                        '</div>' +
		                        '<div class="block_content">' +
		                           '<h2 class="title">' +
		                             '<a>'+ data['error_msg'][i]['task_name'] +'</a>' +
		                           '</h2>' +
		                          '<div class="byline">' +
		                            '<span>'+ data['error_msg'][i]['create_time'] +'</span> by <a>'+ user_name + '</a>' +
		                          '</div>' +
		                          '<pre>' + data['error_msg'][i]['task_msg'] + '</pre>' +
		                        '</div>' +
		                      '</div>' +
		                    '</li>'
		     err_li_strs = err_li_strs + err_li_str
	    }	
	    
	    for (var i=0; i<data['stats_msg'].length; i++){
			var stats_li_str = '<li>' +
		                      '<div class="block">' +
		                        '<div class="tags">' +
		                          '<a href="" class="tag">' +
		                            '<span>任务汇总</span>' +
		                          '</a>' +
		                        '</div>' +
		                        '<div class="block_content">' +
		                           '<h2 class="title">' +
		                             '<a>APPLY TASK PLAY RECAP</a>' +
		                           '</h2>' +
		                          '<div class="byline">' +
		                            '<span>'+ get_dict_default_value(data['stats_msg'][i]['create_time']) +'</span> by <a>'+ user_name + '</a>' +
		                          '</div>' +
		                          '<pre>' + get_dict_default_value(data['stats_msg'][i]['task_msg']) + '</pre>' +
		                        '</div>' +
		                      '</div>' +
		                    '</li>'
		     stats_li_strs = stats_li_strs + stats_li_str
	    }	    
	    
	    for (var i=0; i<data['lastest_msg'].length; i++){
			var lastest_li_str = '<li>' +
		                      '<div class="block">' +
		                        '<div class="tags">' +
		                          '<a href="" class="tag">' +
		                            '<span>最近任务</span>' +
		                          '</a>' +
		                        '</div>' +
		                        '<div class="block_content">' +
		                           '<h2 class="title">' +
		                             '<a>'+ data['lastest_msg'][i]['task_name'] +'</a>' +
		                           '</h2>' +
		                          '<div class="byline">' +
		                            '<span>'+ get_dict_default_value(data['lastest_msg'][i]['create_time']) +'</span> by <a>'+ user_name + '</a>' +
		                          '</div>' +
		                          '<pre>' + get_dict_default_value(data['lastest_msg'][i]['task_msg']) + '</pre>' +
		                        '</div>' +
		                      '</div>' +
		                    '</li>'
		     lastest_li_strs = lastest_li_strs + lastest_li_str
	    }	    
	    
	    if(stats_li_strs.length > 0 || err_li_strs.length > 0 || lastest_li_strs.length > 0){
	    	$("#apply_task_view_li").html('<ul class="list-unstyled timeline" id="apply_task_view_li">'+ lastest_li_strs + err_li_strs + stats_li_strs + '</ul>')
	    }
	    
	});
    
	$('#apply_tasks_table_list tbody').on('click',"button[name='btn-task-delete']",function(){
		var vIds = $(this).val();  
		$.confirm({
		    title: '删除确认',
		    content: '确认删除这条任务?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/apply/task/"+ vIds + "/", 
					type:"DELETE",  		
					success:function(response){
						RefreshTasksLogsTable('apply_tasks_table_list', '/api/apply/tasks/')											
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
		        }			        
		    }
		});			  		 	
    });	  
 
	$('#apply_tasks_table_list tbody').on('click',"button[name='btn-task-tag']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '资产标签同步',
		    content: '确认同步资产标签【'+ name +'】到部署成功的主机?',
		    type: 'blue',
		    buttons: {
		        同步: function () {		       
				$.ajax({
					url:"/api/apply/sync/tag/"+ vIds + "/", 
					type:"POST",  		
					success:function(response){
		            	new PNotify({
		                    title: 'Success!',
		                    text: '标记成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });																
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
		        }			        
		    }
		});			  		 	
    });    
    
    $('#apply_tasks_table_list tbody').on('click', 'td.details-control', function () {
    	var table = $('#apply_tasks_table_list').DataTable();
    	var dataList = [];
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        aId = row.data()["id"];
        $.ajax({
            url : "/api/apply/task/"+aId+"/",
            type : "get",
            async : false,
            dataType : "json",
            success : function(result) {
            	dataList = result;
            }
        });	        
        if ( row.child.isShown() ) {
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            row.child( format_task_result(dataList) ).show();
            tr.addClass('shown');
        }
    });    
		
})