var taskStatusHtml = {
		"0":'<span class="label label-info">进行中</span>',
	    "1":'<span class="label label-success">已完成</span>',
	    "2":'<span class="label label-danger">执行失败</span>',
	    "3":'<span class="label label-warning">执行超时</span> '
	}

var taskTypeHtml = {
	    "0":'<b>部署任务</b>',
	    "1":'<b>数据导出</b>',
	    "2":'<b>binlog解析</b>',
	}

$(document).ready(function() {
	
	var currentUser = $("#currentUser").val()
	
    if ($("#tasksLists").length) {
    	
        $("button[name^='tasks_page_']").on("click", function(){
          	var url = $(this).val();
          	$(this).attr("disabled",true);
          	if (url.length){
          		RefreshTable('tasksLists', url, 'tasks');
          	}      	
        	$(this).attr('disabled',false);
          }); 
    	    	
    	function makeTaskTableList(){
		    var columns = [	       
			               	{
			               		"className":      'details-control',
			                    "orderable":      false,
			                    "data":           null,
			                    "defaultContent": ''
			                },			    	
		                    {"data": "id"},
		                    {"data": "type"},
		                    {"data": "task_name"},		              
			                {"data": "user"},	
			                {"data": "args"},	
			                {"data": "status"},
			                {"data": "ctime","className": "text-center",},
			                {"data": "etime","className": "text-center",},			                			                
			               ]
		    var columnDefs = [			                      
								{
									targets: [2],
									render: function(data, type, row, meta) {
										return taskTypeHtml[row.type]
									},
								},	
								{
									targets: [6],
									render: function(data, type, row, meta) {
										return taskStatusHtml[row.status]
									},
								},									
	    	    		        {
		    	    				targets: [9],
		    	    				render: function(data, type, row, meta) {	
		    	    					if (userInfo[currentUser]["is_superuser"]){
		    	    						var edit = '<button type="button" name="btn-task-delete" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var edit = ''
		    	    					}		    	    					
		    	    					if (row.status == 0){
			    	                        return '<div class="btn-group  btn-group-sm">' +		
			    	                           '<button type="button" name="btn-task-stop" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-play-circle-o" aria-hidden="true"></span></button>' + edit +
			    	                           '</div>';
		    	    					}else{
			    	                        return '<div class="btn-group  btn-group-sm">' +		
			    	                           '<button type="button" name="btn-task-stop" class="btn btn-default"  aria-label="Justify" disabled><span class="fa fa-play-circle-o" aria-hidden="true"></span></button>'  + edit +
			    	                           '</div>';		    	    						
		    	    					}

		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    var buttons = [					    
					    
		    ] 		    
		    InitDataTable('tasksLists','/api/account/user/task/',buttons,columns,columnDefs,'tasks');   		
    	}
    	
    	makeTaskTableList()
    	
    	var table = $('#tasksLists').DataTable();
    	
    	$('#tasksLists tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );	        
	        aId = row.data()["id"];
	        $.ajax({
	        	url: "/api/account/user/task/"+ aId +"/",
	            type : "get",
	            async : false,
	            success : function(result) {
	            	dataList = result;
	            }
	        });	  
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child(taskInfoFormat(dataList)).show();
	            tr.addClass('shown');
	        }       
	    });    	
    	
    	$('#tasksLists tbody').on('click','button[name="btn-task-stop"]',function(){
    		var vIds = $(this).val();
    	    $.confirm({
    	        icon: 'fa fa-times',
    	        type: 'blue',
    	        title: '任务终止',
    	        content: '<div class="form-group"><input type="text" value="" placeholder="请输入终止原因" class="param_name form-control" /></div>',
    	        buttons: {
    	            '取消': function() {},
    	            '停止': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                    var cancel = this.$content.find('.param_name').val();
    				    	$.ajax({  
    				            cache: true,  
    				            type: "POST",  
    				            url:"/api/account/user/task/" + vIds + '/', 
    				            data:{
    								"action":"stop",
    								"msg":cancel
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
    				                    text: '任务终止成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	RefreshTable('tasksLists', '/api/account/user/task/', 'tasks');
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });	
    	});   
    	
    	$('#tasksLists tbody').on('click','button[name="btn-task-delete"]',function(){
    		var vIds = $(this).val();
    	  	var td = $(this).parent().parent().parent().find("td")
        	var task = td.eq(3).text()
    	  	
    		$.confirm({
    		    title: '删除确认',
    		    content:  task,
    		    type: 'red',
    		    buttons: {
    		             删除: function () {
    		    	$.ajax({  
    		            cache: true,  
    		            type: "DELETE",  
    		            url:'/api/account/user/task/'+ vIds + '/' ,    
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
    		            	RefreshTable('tasksLists', '/api/account/user/task/', 'tasks');   
    		            }  
    		    	});
    		        },
    		        取消: function () {
    		            return true;			            
    		        },			        
    		    }
    		});	
    	}); 
    	    	
	}	
	
})
