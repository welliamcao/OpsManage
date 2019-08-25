$(function(){
    $("#project_name").on("input",function(e){
    	$("#project_dir").attr("value",'/var/lib/opsmanage/workspaces/release/'+e.delegateTarget.value+'/');
    	$("#project_repo_dir").attr("value",'/var/lib/opsmanage/workspaces/source/'+e.delegateTarget.value+'/');
    	$("#dir").attr("value",'/var/www/'+e.delegateTarget.value+'/');
    });
    
});

function format ( data ) {
	var serHtml = '';
	serList = data["number"];
	for  (var i=0; i <serList.length; i++){
		serHtml += serList[i]['ip'] + ',';
	}
    var trHtml = '<tr><td>打包目录:</td><td>'+ data["project_dir"]  + '</td><td>源代码目录:</td><td>'+ data["project_repo_dir"] +'</td></tr>'	;
    trHtml += '<tr><td>远程命令:</td><td>'+ data["project_remote_command"]  + '</td><td>目标服务器:</td><td>'+ serHtml.substring(0,serHtml.length-1) +'</td></tr>';
    trHtml += '<tr><td>远程路径:</td><td>'+ data["project_target_root"]  + '</td><td>目录宿主:</td><td>'+ data["project_user"] +'</td></tr>';	
    trHtml += '<tr><td>排除文件:</td><td>'+ data["project_exclude"]  + '</td><td>日志目录:</td><td>'+ data["project_logpath"] +'</td></tr>';	    
	if (data["project_type"]=='compile'){
		trHtml += '<tr><td>编译类型:</td><td>编译型</td><td>编译命令:</td><td>'+ data["project_local_command"].replace(/\r\n/g,'<br>') +'</td></tr>';	   
	}else{
		trHtml += '<tr><td>编译类型:</td><td>非编译型</td><td>编译命令:</td><td></td></tr>';	   
	}	    
    var vHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
    			'<legend>'+ data["project_name"] +'部署信息</legend>' +
    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
    				  trHtml  +
    				'</table>'
    		    '</div>'; 				
    return vHtml;
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
		"sSearch" : "搜索:",
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



function setAceEditMode(ids,model,theme) {
	try
	  {
		var editor = ace.edit(ids);
		require("ace/ext/old_ie");
		var langTools = ace.require("ace/ext/language_tools");
		editor.removeLines();
		editor.setTheme(theme);
		editor.getSession().setMode(model);
		editor.setShowPrintMargin(false);
		editor.setOptions({
		    enableBasicAutocompletion: true,
		    enableSnippets: true,
		    enableLiveAutocompletion: true
		}); 
	 	return editor
	  }
	catch(err)
	  {
		console.log(err)
	  }

			 
};

function oBtProjectSelect(){
	   $('#deploy_service').removeAttr("disabled");
	   var obj = document.getElementById("deploy_project"); 
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/project/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="deploy_service" id="deploy_service" onchange="javascript:AssetsTypeSelect();" required><option selected="selected" name="deploy_service" value="">请选择业务类型</option>'
					var selectHtml = '';
					for (var i=0; i <response["service_assets"].length; i++){
						 selectHtml += '<option name="deploy_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					document.getElementById("deploy_service").innerHTML= binlogHtml;	
						
				},
			});	
	   }
	   else{
		   $('#deploy_service').attr("disabled",true);
	   }
}

function AssetsTypeSelect(model,ids){
	   var obj = document.getElementById(ids); 
	   var index = obj.selectedIndex;
	   var sId = obj.options[index].value; 
	   if ( sId  > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/assets/server/query/', //请求地址
				type:"POST",  //提交类似
				data:{
					"query":model,
					"id":sId
				},
				success:function(response){
					var binlogHtml = '<select  class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="server" id="server" required><option  name="server" value="">请选择服务器</option>'
						var selectHtml = '';
						for (var i=0; i <response["data"].length; i++){
							 selectHtml += '<option name="server" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + '</option>' 
						};                        
						binlogHtml =  binlogHtml + selectHtml + '</select>';
						document.getElementById("server").innerHTML= binlogHtml;	
						$('.selectpicker').selectpicker('refresh');	
				
						
				},
			});	
	   }
}


function draw_apps_graph_bar(ids,dataList) {
	$("#"+ids).length && Morris.Bar({
        element: ids,
        data: dataList,
        xkey: "name",
        ykeys: ["count"],
        labels: ["总计"],
        barRatio: .4,
        barColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        xLabelAngle: 35,
        hideHover: "auto",
        resize: !0
    })	
}

function draw_apps_graph_pie(ids,dataList){
	$("#"+ids).length && Morris.Donut({
	    element: ids,
	    data: dataList,
	    colors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
	    formatter: function(a) {
	        return a + "%"
	    },
	    resize: !0
	})	
}

function draw_apps_graph_line(ids,dataList){
	 $("#"+ids).length && (Morris.Line({
	        element: ids,
	        xkey: "dtime",
	        ykeys: ["value"],
	        labels: ["Value"],
	        hideHover: "auto",
	        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
	        data: dataList,
	        resize: !0
	    }), $MENU_TOGGLE.on("click",
	    function() {
	        $(window).resize()
	    }))
}

$(document).ready(function() {
	$(function() {
		var respone = requests("get","/api/apps/count/")
		draw_apps_graph_bar("all_apps_graph_bar",respone["releaseCount"])
		draw_apps_graph_pie("all_apps_graph_pie",respone["successRate"])
		draw_apps_graph_line("all_apps_graph_line",respone["monthCount"])		
	})	

	
	function InitDataTable(tableId,url,columns,columnDefs){
	  oOverviewTable =$('#'+tableId).dataTable({
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	requests('get',url),
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    			
		    	});
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
	  });
	}

	function AutoReload(tableId,url){
	  RefreshTable('#'+tableId, url);
	  setTimeout(function(){AutoReload(url);}, 30000);
	}	
	
/*	 $("#project_env").change(function(){
		   var obj = document.getElementById("project_env"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   if (value=="uat"){
			   $("#extConfig").show();  	   
		   }
		   else {
			   $("#extConfig").hide();  
		   }		 
	 });*/
	 
	 $("#project_repertory").change(function(){
		   var project_model = '<select class="form-control" id="project_model" name="project_model" required>' +
								'<option selected="selected" value="">选择上线版本控制类型</option>' +
								'<option value="tag" name="project_model">Tag</option>'
		   var obj = document.getElementById("project_repertory"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   if (value=="svn"){
			   $("#repo_type").show();  
			   $("#project_model").html(project_model + '<option value="trunk" name="project_model">Trunk</option></select>')
		   }
		   else {
			   $("#repo_type").hide();
			   $("#project_model").html(project_model + '<option value="branch" name="project_model">Branch</option>')
		   }
	});	 
	
	var compile_type = 'noncompile';
	if ($("#project_local_command").length){
		var aceEditAdd = setAceEditMode("project_local_command","ace/mode/sh","ace/theme/terminal");
	}		
	
	try
		{
			$("button[name='compile_type']").click(function(){
				compile_type = $(this).val()
				if (compile_type=='compile'){
					$("#compile").show()
				}
				else{
					$("#compile").hide()
				}
					
			});			  
		}
	catch(err)
		{
			console.log(err)
		}	
	
    $('#btn_add_project').click(function(){ 
		var btnObj = $(this);
		btnObj.attr('disabled',true);
    	var required = ["deploy_project","deploy_service","project_name","project_env","project_repertory","project_address","server","project_user","dir"];
    	btnObj.attr('disabled',true);
    		var form = document.getElementById('add_deploy_project');
    		for (var i = 0; i < form.length; ++i) {
    			var name = form[i].name;
    			var value = form[i].value;	
    			idx = $.inArray(name, required);						
    			if (idx >= 0 && value.length == 0){
                	new PNotify({
                        title: 'Warning!',
                        text: '请注意必填项不能为空~',
                        type: 'warning',
                        styling: 'bootstrap3'
                    }); 
    				btnObj.removeAttr('disabled');
    				return false;
    			};					
    		};				
    	    var formData = new FormData();	
    		var serverList = new Array();
    		$("#server option:selected").each(function () {
    			serverList.push($(this).val())
    		})	   
    		formData.append('type','create');	
    	    formData.append('project_env',$('#project_env').val());	
    	    formData.append('project_name',$('#project_name').val());	 
    	    formData.append('project_address',$('#project_address').val());	
    	    formData.append('project_user',$('#project_user').val());
    	    formData.append('dir',$('#dir').val());	
    	    formData.append('project_remote_command',$('#project_remote_command').val());
    	    formData.append('project_pre_remote_command',$('#project_pre_remote_command').val());
    	    formData.append('project_exclude',$('#project_exclude').val());	
    	    formData.append('project_dir',$('#project_dir').val());	
    	    formData.append('logpath',$('#logpath').val());
    	    formData.append('project_repo_dir',$('#project_repo_dir').val());
    	    formData.append('project_repo_user',$('#project_repo_user').val());	
    	    formData.append('project_repo_passwd',$('#project_repo_passwd').val());
    	    formData.append('project_audit_group',$('#project_audit_group  option:selected').val());	
    	    formData.append('project_id',$('#deploy_project option:selected').val());
    	    formData.append('project_service',$('#deploy_service option:selected').val());
    	    formData.append('project_repertory',$('#project_repertory option:selected').val());
    	    formData.append('project_model',$('#project_model option:selected').val());	
    	    formData.append('server',serverList);	
    	    formData.append('project_local_command',aceEditAdd.getSession().getValue());
    	    formData.append('project_type',compile_type);
    		$.ajax({
    			url:'/apps/config/', //请求地址
    			type:"POST",  //提交类似
    		    processData: false,
    		    contentType: false,				
    			data:formData,  //提交参数
    			success:function(response){
    				btnObj.removeAttr('disabled');				
    				if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: "添加成功",
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
    		});	    	
    });		
	
    if ($("#projectList").length) {
    	function makeProjectList(){
		    var columns = [
				            {
				                "className": 'details-control',
				                "orderable": false,
				                "data":      null,
				                "defaultContent": ''
				            },
		                    {"data": "id"},
			                {"data": "project_business_paths"},
			                {"data": "project_name"},		
			                {"data": "project_env"},	
			                {"data": "project_repo_dir"},	
			                {"data": "project_address","sClass": "text-center"},
			                {"data": "project_status"},	
			                { "data": "操作" }
			               ]
		    var columnDefs = [		
								{
									targets: [4],
									render: function(data, type, row, meta) {
										if(row.project_env=='uat'){
											var status = '<span class="label label-danger">生产环境</span>'
										}else if(row.project_env=='sit'){
											var status = '<span class="label label-success">测试环境</span>'
										}else{
											var status = '<span class="label label-info">灰度环境</span>'
										}
								        return status
									},
								},		                      
								{
									targets: [7],
									render: function(data, type, row, meta) {
										if(row.project_status==1){
											return '<button type="button" name="btn-project-init" class="btn btn-round btn-success btn-xs">已初始化</button>'
										}else if(row.project_status==0){
											return '<button type="button" name="btn-project-init" class="btn btn-round btn-danger btn-xs" value="'+ row.id +'">点击初始化</button>'
										}
									},
									"className": "text-center",
								},								
	    	    		        {
		    	    				targets: [8],
		    	    				render: function(data, type, row, meta) {
		    	    					if (row.project_repertory=='git' && row.project_model == 'branch'){
		    	    						var branch = '<button type="button" name="btn-project-branch" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-github-alt" aria-hidden="true"></span></button>'
		    	    					}
		    	    					else{
		    	    						var branch = '<button type="button" name="btn-project-branch" value="'+ row.id +'" class="btn btn-default disabled"  aria-label="Justify"><span class="fa fa-github-alt" aria-hidden="true"></span></button>'
		    	    					}
		    	                        return '<div class="btn-group  btn-group-sm">' +	
			    	                           '<button type="button" name="btn-project-run" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><a href="/apps/manage/?type=status&id='+ row.id +'"><span class="fa fa-play" aria-hidden="true"></span></a>' +	
			    	                           '</button>' +			    	                        
			    	                           '<button type="button" name="btn-project-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><a href="/apps/config/?type=edit&id='+ row.id +'"><span class="fa fa-pencil-square-o" aria-hidden="true"></span></a>' +	
			    	                           '</button>' + branch +                			    	                           
			    	                           '<button type="button" name="btn-project-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
			    	                           '</button>' +			                            
			    	                           '</div>';
		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    return InitDataTable('projectList','/api/apps/list/',columns,columnDefs);
		    //每隔30秒刷新table
//		    setTimeout(function(){AutoReload('taskTableList','/api/sched/tasks/');}, 30000);    		
    	}
    	
    	makeProjectList()   	
    	
		
    	
	    $('#projectList tbody').on('click', 'td.details-control', function () {
	    	var table = $('#projectList').DataTable();
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );
	        aId = row.data()["id"];
	        $.ajax({
	            url : "/apps/config/?type=info&id="+aId,
	            type : "get",
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
    	
        $('#projectList tbody').on('click',"button[name='btn-project-init']", function(){
        	var apps_id = $(this).val()
        	var pname = $(this).parent().parent().find("td").eq(3).text();
        	if (apps_id > 0){
        		$.confirm({
        		    title: '操作确认',
        		    content: "确认是否初始项目【<code>"+pname+"</code>】?",
        		    type: 'red',     		    
        		    buttons: {
        		        确认: function () {
        		        	$.ajax({  
        		                cache: true,  
        		                type: "POST",  
        		                url:"/apps/config/",  
        		                data:{
        		                	"type":'init',
        		                	"id":apps_id
        		                },
        		                async: true,  
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
        		                            text: response["msg"],
        		                            type: 'success',
        		                            styling: 'bootstrap3'
        		                        }); 
        		                    	RefreshTable('#projectList', '/api/apps/list/');
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
        		        },  		        
        		        取消: function () {
        		            return true;			            
        		        },         		        
        		    },
      		    
        		});	      		
        	}else{
        		$.dialog({
        		    title: '错误信息!',
        		    content: '项目已经初始化!',
        		});    		
        	}
        	
        })    	
    	
	}

    $('#projectList tbody').on('click',"button[name='btn-project-branch']", function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(3).text();
		var env = $(this).parent().parent().parent().find("td").eq(4).text(); 
		var btnObj = $(this);
		btnObj.attr('disabled',true);		
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: env + '<code>' + name + '</code>' + '远程分支',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">远程分支 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="modf_type_name" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +		                        
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '切换': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find("[name='modf_type_name']").val();
				    	$.ajax({  
				            cache: true,  
				            type: "POST",  
				            url:"/apps/manage/",  
				            data:{
				            		"name":param_name,
				            		"id":vIds,
				            		"type":"create_branch"
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
				                    text: '添加成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            }  
				    	});
				    	btnObj.attr('disabled',false);		
	                }
	            }
	        }
	    });		  		 	
    });	     
    
    $('#projectList tbody').on('click',"button[name='btn-project-delete']", function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(3).text();
		var env = $(this).parent().parent().parent().find("td").eq(4).text(); 
		$.confirm({
		    title: '删除确认',
		    content:    "【" + env +"】" + '<strong> <code>' + name + '</code></strong>项目',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:'/api/apps/list/'+ vIds +'/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
//			            window.location.reload();
			            RefreshTable('#projectList', '/api/apps/list/');
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
    
})

