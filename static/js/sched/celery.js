function isJsonString(str) {
      	try {
            if (typeof JSON.parse(str) == "object") {
                return true;
            }
        } catch(e) {
        }
        return false;
    }

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
}

function make_crontab_select(){
    $.ajax({  
        url : '/api/sched/crontab/',  
        type : 'get', 
        success : function(response){
        		$('#div_crontab').show()
        		$('#div_interval').hide()
				$("#select-crontab").empty()
				var crontabHtml = '<select class="form-control" name="crontab" id="select-crontab" required="required">'
				var selectHtml = ''; 
				for (var i=0; i <response.length; i++){
					 selectHtml += '<option name="crontab" value="'+ response[i]["id"] +'">' + response[i]["minute"] + '&nbsp;' + 
					                response[i]["hour"] + '&nbsp;' + response[i]["day_of_week"]  + '&nbsp;' + response[i]["day_of_month"] + 
					                '&nbsp;' + response[i]["month_of_year"] +'</option>' 
				};                        
				crontabHtml =  crontabHtml + selectHtml + '</select>';
				$("#select-crontab").html(crontabHtml);			            	
	            },
	    	error:function(response){
	    		console.log(response)
	    	}	            
    });		
}

function make_interval_select(){
    $.ajax({  
        url : '/api/sched/intervals/',  
        type : 'get', 
        success : function(response){
        		$('#div_crontab').hide()
        		$('#div_interval').show()
				$("#select-interval").empty();
				var intervalHtml = '<select class="form-control" name="crontab" id="select-interval" required="required">'
				var selectHtml = ''; 
				for (var i=0; i <response.length; i++){
					 selectHtml += '<option name="interval" value="'+ response[i]["id"] +'">' + response[i]["every"] + '&nbsp;' + response[i]["period"] + '</option>' 
				};                        
				crontabHtml =  intervalHtml + selectHtml + '</select>';
				$("#select-interval").html(crontabHtml);				        		
            	
            },
	    	error:function(response){
	    		console.log(response)
	    	}	            
    });	
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


function InitDataTable(tableId,url,buttons,columns,columnDefs)
{
  oOverviewTable =$('#'+tableId).dataTable(
		  {
			  	"dom": "Bfrtip",
	    		"bScrollCollapse": false, 				
	    	    "bRetrieve": true,			
	    		"destroy": true, 
	    		"buttons" :buttons, 	    		
	    		"data":	requests('get',url),
	    		"columns": columns,
	    		"columnDefs" :columnDefs,			  
	    		"language" : language,
	    			
	    	});
}

function RefreshTable(tableId, urlData)
{
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
  });
}

function AutoReload(tableId,url)
{
  RefreshTable('#'+tableId, url);
  setTimeout(function(){AutoReload(url);}, 30000);
}

$(document).ready(function() {	
	
    $("#add_interval_button").click(function(){
    	$('#modfInterval').val("").hide()
    	$('#addInterval').show()
    }); 	

    $("#add_crontab_button").click(function(){
    	$('#modfCrontab').val("").hide()
    	$('#addCrontab').show()
    });     
    
    if ($("#taskTableList").length) {
    	function makeTaskList(){
		    var columns = [
		                    {"data": "id"},
			                {"data": "name"},
			                {"data": "task"},		
			                {"data": "kwargs"},	
			                {"data": "last_run_at"},	
			                {"data": "total_run_count","sClass": "text-center"},
			                {"data": "enabled","sClass": "text-center"},	
			               ]
		    var buttons = [{
                text: '<span class="fa fa-plus"></span>',
                className: "btn-xs",
                action: function ( e, dt, node, config ) {
                	$('#addTaskModal').modal("show");	
                }
			}]	
		    var columnDefs = [	
								{
									targets: [5],
									render: function(data, type, row, meta) {
								        return '<span class="badge badge-warning">'+ row.total_run_count +'</span>'
									},
								},	
								{
									targets: [6],
									render: function(data, type, row, meta) {
										if(row.enabled==1){
											var status = '<span class="label label-success">激活</span>'
										}else if(row.enabled==0){
											var status = '<span class="label label-danger">冻结</span>'
										}
								        return status
									},
								},								
	    	    		        {
		    	    				targets: [7],
		    	    				render: function(data, type, row, meta) {
		    	                        return '<div class="btn-group  btn-group-xs">' +	
			    	                           '<button type="button" name="btn-task-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-pencil-square-o" aria-hidden="true"></span>' +	
			    	                           '</button>' +		                				                            		                            			                          
			    	                           '<button type="button" name="btn-task-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
			    	                           '</button>' +			                            
			    	                           '</div>';
		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    InitDataTable('taskTableList','/api/sched/tasks/',buttons,columns,columnDefs);
		    //每隔30秒刷新table
		    setTimeout(function(){AutoReload('taskTableList','/api/sched/tasks/');}, 30000);    		
    	}
    	makeTaskList()
	    
	}
    
    if ($("#crontabList").length) {
    	function makeCrontabList(){
		    var columns = [
			                {"data": "id"},
			                {"data": "minute"},
			                {"data": "hour"},		
			                {"data": "day_of_week"},	
			                {"data": "day_of_month"},	
			                {"data": "month_of_year","sClass": "text-center"},	
			               ]
		    var buttons = [{
                text: '<span class="fa fa-plus"></span>',
                className: "btn-xs",
                action: function ( e, dt, node, config ) {
                	$('#modfCrontab').val("").hide()
                	$("#addCrontabModal").modal("show")
                }
			}]		    
		    var columnDefs = [					               
	    	    		        {
	    	    				targets: [6],
	    	    				render: function(data, type, row, meta) {
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-crontab-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-pencil-square-o" aria-hidden="true"></span>' +	
		    	                           '</button>' +		                				                            		                            			                          
		    	                           '<button type="button" name="btn-crontab-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
		    	                           '</button>' +			                            
		    	                           '</div>';
	    	    				},
	    	    				"className": "text-center",
	    	    			}]
		    
		    InitDataTable('crontabList','/api/sched/crontab/',buttons,columns,columnDefs);
		    //每隔30秒刷新table
		    //setTimeout(function(){AutoReload('crontabList','/api/sched/crontab/');}, 30000);    		
    	}
    	makeCrontabList()
	    
	}     
    
    if ($("#intervalList").length) {
    	function makeIntervalList(){
		    var columns = [
		                {"data": "id"},
		                {"data": "every"},
		                {"data": "period"},		                				                
		               ]
		    var buttons = [{
                text: '<span class="fa fa-plus"></span>',
                className: "btn-xs",
                action: function ( e, dt, node, config ) {
			    	$('#modfInterval').val("").hide()
			    	$('#addIntervalModal').modal("show")
                }
			}]			    
		    var columnDefs = [					               
	    	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-interval-edit" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-pencil-square-o" aria-hidden="true"></span>' +	
		    	                           '</button>' +		                				                            		                            			                          
		    	                           '<button type="button" name="btn-interval-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
		    	                           '</button>' +			                            
		    	                           '</div>';
	    	    				},
	    	    				"className": "text-center",
	    	    			}]
		    
		    InitDataTable('intervalList','/api/sched/intervals/',buttons,columns,columnDefs);
		    //每隔30秒刷新table
		    //setTimeout(function(){AutoReload('intervalList','/api/sched/intervals/');}, 30000);
      }
    	makeIntervalList()
	}     
        
    
    $('#addInterval').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);		
		$.ajax({
			url:'/api/sched/intervals/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    datatype:"JSON",				
			data:$("#addIntervalForm").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				RefreshTable('#intervalList', '/api/sched/intervals/');
            	new PNotify({
                    title: 'Success!',
                    text: "添加成功",
                    type: 'success',
                    styling: 'bootstrap3'
                });				
				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "添加失败",
                    text: response,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });
    
    $('#addCrontab').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);		
		$.ajax({
			url:'/api/sched/crontab/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    datatype:"JSON",				
			data:$("#addCrontabForm").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled'); 				
				RefreshTable('#crontabList', '/api/sched/crontab/');	
            	new PNotify({
                    title: 'Success!',
                    text: "添加成功",
                    type: 'success',
                    styling: 'bootstrap3'
                });				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "添加失败",
                    text: response,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });
    
	$('#intervalList tbody').on('click',"button[name='btn-interval-edit']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
	    $.ajax({  
	        url : '/api/sched/intervals/'+ vIds + '/',  
	        type : 'get', 
	        success : function(response){
	            	btnObj.removeAttr('disabled');
	            	$('#interval_every').val(response['every'])
	            	DynamicSelect('interval_period',response['period'])
	            	$('#addIntervalModal').modal('toggle');	            	
	            	$('#addInterval').hide()
	            	$('#modfInterval').val(vIds).show()
	            },
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: "数据不存在或者已经被删除",
	                    text: response,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 		    		
		    	}	            
	    });		
	});    
		
	$('#intervalList tbody').on('click',"button[name='btn-interval-delete']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		var every = $(this).parent().parent().parent().find("td").eq(1).text(); 
		var period = $(this).parent().parent().parent().find("td").eq(2).text();
		$.confirm({
		    title: '删除确认',
		    content: period + ': ' + every + '<br><strong>[注]:此操作会删除关联的Celery任务</strong>',
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
				    dataType: "json",
					data:{
						"id":vIds,
					}, 		            
		            url:'/api/sched/intervals/'+ vIds + '/',   
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
		            	RefreshTable('#intervalList', '/api/sched/intervals/');
		            }  
		    	});
		        },
		        取消: function () {
		        	btnObj.removeAttr('disabled');
		            return true;			            
		        },			        
		    }
		});		
	}); 	
	
	$('#crontabList tbody').on('click',"button[name='btn-crontab-edit']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
	    $.ajax({  
	        url : '/api/sched/crontab/'+ vIds + '/',  
	        type : 'get', 
	        success : function(response){
	            	btnObj.removeAttr('disabled');
	            	$('#crontab_minute').val(response['minute'])
	            	$('#crontab_hour').val(response['hour'])
	            	$('#crontab_day_of_week').val(response['day_of_week'])
	            	$('#crontab_day_of_month').val(response['day_of_month'])
	            	$('#crontab_month_of_year').val(response['month_of_year'])
	            	$('#addCrontabModal').modal('toggle');
	            	$('#addCrontab').hide()
	            	$('#modfCrontab').val(vIds).show()	            	
	            },
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: "数据不存在或者已经被删除",
	                    text: response,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 		    		
		    	}	            
	    });		
	});  	
    
	$('#crontabList tbody').on('click',"button[name='btn-crontab-delete']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		$.confirm({
		    title: '删除确认',
		    content: '删除id为：（' + vIds + '）的任务调度  <br><strong>[注]:此操作会删除关联的Celery任务</strong>',
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
				    dataType: "json",
					data:{
						"id":vIds,
					}, 		            
		            url:'/api/sched/crontab/'+ vIds + '/',   
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
		            	RefreshTable('#crontabList', '/api/sched/crontab/');
		            }  
		    	});
		        },
		        取消: function () {
		        	btnObj.removeAttr('disabled');
		            return true;			            
		        },			        
		    }
		});		
	});	
	
    $('#modfInterval').on('click', function() {
		var btnObj = $(this);
		var vIds = $(this).val();
		btnObj.attr('disabled',true);	
		$.ajax({
			url: '/api/sched/intervals/'+ vIds + '/', //请求地址
			type:"PUT",  //提交类似
		    processData: false,
		    datatype:"JSON",				
			data:$("#addIntervalForm").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				RefreshTable('#intervalList', '/api/sched/intervals/');		
            	new PNotify({
                    title: '<strong>操作成功:</strong>',
                    text: "修改成功",
                    type: 'success',
                    styling: 'bootstrap3'
                }); 				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "修改失败",
                    text: response,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });	
    
    $('#modfCrontab').on('click', function() {
		var btnObj = $(this);
		var vIds = $(this).val();
		btnObj.attr('disabled',true);	
		$.ajax({
			url: '/api/sched/crontab/'+ vIds + '/', //请求地址
			type:"PUT",  //提交类似
		    processData: false,
		    datatype:"JSON",				
			data:$("#addCrontabForm").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				RefreshTable('#crontabList', '/api/sched/crontab/');		
            	new PNotify({
                    title: '<strong>操作成功:</strong>',
                    text: "修改成功",
                    type: 'success',
                    styling: 'bootstrap3'
                }); 				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "修改失败",
                    text: response,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });	   
	 
    var select_type = ''
	$("#schetype").change(function(){
		 var obj = document.getElementById("schetype"); 
		 var index = obj.selectedIndex;
		 select_type = obj.options[index].value; 	
		   if (select_type=="select_crontab"){
			   make_crontab_select()	   
		   }else if(select_type=="select_interval"){
			   make_interval_select()			   			   
		   }		 
	 }); 

    $('#add_task_button').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);
		var formData = new FormData();
		if (select_type=="select_crontab"){
			formData.append('crontab',$('#select-crontab option:selected').val());
		}else if(select_type=="select_interval"){
			formData.append('interval',$('#select-interval option:selected').val());
		}
		formData.append('task',$('#task option:selected').val());
		formData.append('name',$('#task_name').val());
		formData.append('args',$('#args').val());
		formData.append('kwargs',$('#kwargs').val());
		formData.append('queue',$('#queue').val());
		formData.append('expires',$('#expires').val());
		formData.append('enabled',$('#enabled option:selected').val());
		$.ajax({
			url: '/api/sched/tasks/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,			
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
				RefreshTable('#taskTableList', '/api/sched/tasks/');		
            	new PNotify({
                    title: '<strong>操作成功:</strong>',
                    text: "添加成功",
                    type: 'success',
                    styling: 'bootstrap3'
                }); 				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "添加失败",
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });	    
    
	$('#taskTableList tbody').on('click',"button[name='btn-task-edit']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
	    $.ajax({  
	        url : '/api/sched/tasks/'+ vIds + '/',  
	        type : 'get', 
	        success : function(response){
	            	btnObj.removeAttr('disabled');
//	            	$('#interval_every').val(response['every'])
//	            	DynamicSelect('interval_period',response['period'])
	            	$('#task_name').val(response['name'])
	            	DynamicSelect('task',response['task'])
	            	//$('#task').attr('disabled',true);	
	            	$('#args').val(response['args']);
	            	$('#kwargs').val(response['kwargs']);
	            	$('#queue').val(response['queue']);
	            	$('#expires').val(response['expires']);
	            	if (response['crontab'] > 0){
	            		make_crontab_select()	            		
	            		DynamicSelect('schetype','select_crontab')
		        		DynamicSelect('select-crontab',response['crontab'])
	            	}else if(response['interval'] > 0){
	            		make_interval_select()
	            		DynamicSelect('schetype','select_interval')
		        		DynamicSelect('select-interval',response['interval'])	            		
	            	}
	            	if (response['enabled']){
	            		DynamicSelect('enabled',1)
	            	}else{
	            		DynamicSelect('enabled',0)
	            	}	            	
	            	$('#addTaskModal').modal('toggle');	            	
	            	$('#add_task_button').hide()
	            	$('#modf_task_button').val(vIds).show()
	            },
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: "数据不存在或者已经被删除",
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 		    		
		    	}	            
	    });		
	});  
	
    $('#modf_task_button').on('click', function() {
		var btnObj = $(this);
		var vIds = $(this).val();
		btnObj.attr('disabled',true);
		var formData = new FormData();
		if (select_type=="select_crontab"){
			formData.append('crontab',$('#select-crontab option:selected').val());
			formData.append('interval','');
		}else if(select_type=="select_interval"){
			formData.append('interval',$('#select-interval option:selected').val());
			formData.append('crontab','');
		}
		formData.append('task',$('#task option:selected').val());
		formData.append('name',$('#task_name').val());
		formData.append('args',$('#args').val());
		formData.append('kwargs',$('#kwargs').val());
		formData.append('queue',$('#queue').val());
		formData.append('expires',$('#expires').val());
		formData.append('enabled',$('#enabled option:selected').val());		
		$.ajax({
			url: '/api/sched/tasks/'+ vIds + '/', //请求地址
			type:"PUT",  //提交类似
		    processData: false,
		    contentType: false,			
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				RefreshTable('#taskTableList', '/api/sched/tasks/');		
            	new PNotify({
                    title: '<strong>操作成功:</strong>',
                    text: "修改成功",
                    type: 'success',
                    styling: 'bootstrap3'
                }); 				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
            	new PNotify({
                    title: "修改失败",
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	    		
	    	}
		})	    	
    });	
    
	$('#taskTableList tbody').on('click',"button[name='btn-task-delete']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		var task_name = $(this).parent().parent().parent().find("td").eq(1).text();
		$.confirm({
		    title: '删除确认',
		    content: task_name,
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
				    dataType: "json",
					data:{
						"id":vIds,
					}, 		            
		            url:'/api/sched/tasks/'+ vIds + '/',   
		            error: function(request) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response.responseText,
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
		            	RefreshTable('#taskTableList', '/api/sched/tasks/');
		            }  
		    	});
		        },
		        取消: function () {
		        	btnObj.removeAttr('disabled');
		            return true;			            
		        },			        
		    }
		});		
	});	    
    
})