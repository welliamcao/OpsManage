function isJsonString(data) {
    try {
        if (typeof JSON.parse(data)) {
            return true;
        }
    } catch(e) {
    }
    return false;
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

function randomNum(minNum,maxNum){ 
    switch(arguments.length){ 
        case 1: 
            return parseInt(Math.random()*minNum+1,10); 
        break; 
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
        break; 
            default: 
                return 0; 
            break; 
    } 
} 

function random_star(random_number){
	var a_str = ''
	for (var i = 0; i < 5; ++i) {
		if ( i < random_number){
			var a = '<a href="#"><span class="fa fa-star"></span></a>'
		}
		else{
			var a = '<a href="#"><span class="fa fa-star-o"></span></a>'
		}
		a_str =  a_str + a
	}
	return a_str
}

function oBtProjectSelect(obj){
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   apply_hosts["hosts"] = []
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/business/nodes/assets/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var sHtml = '';
					for (var i=0; i <response.length; i++){
						apply_hosts["hosts"].push(response[i]["detail"]["ip"])
						sHtml += '<br>' + response[i]["detail"]["ip"]
					};  
					if ( sHtml.length > 0){
		            	new PNotify({
		                    title: "<strong>发现主机:</strong>",
		                    text: sHtml,
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });
		                $("#add_task_apply_hosts").val(JSON.stringify(apply_hosts,null, 2))
					}
					else {
		            	new PNotify({
		                    title: "<strong>Ops：</strong>",
		                    text: "该条件下未发现主机资源~",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 	
					}						
				},
			});	
	   }
}

function oBtInventorySelect(obj){
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/inventory/groups/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="inventory_groups"  onchange="javascript:AssetsTypeSelect(this,"inventory_groups");" required><option selected="selected"  value="">请选择主机组</option>'
					var selectHtml = '';
					for (var i=0; i <response["data"].length; i++){
						 selectHtml += '<option value="'+ response["data"][i]["id"] +'">' + response["data"][i]["name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("select[name='inventory_groups']").html(binlogHtml)
					$("select[name='inventory_groups']").selectpicker('refresh');					
						
				},
			});	
	   }
	   else{
		   $('#deploy_service').attr("disabled",true);
	   }
}

function oBtInventorySelect(obj){
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/inventory/groups/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="inventory_groups"  onchange="javascript:AssetsTypeSelect(this,"inventory_groups");" required><option selected="selected"  value="">请选择主机组</option>'
					var selectHtml = '';
					for (var i=0; i <response["data"].length; i++){
						 selectHtml += '<option value="'+ response["data"][i]["id"] +'">' + response["data"][i]["name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("select[name='inventory_groups']").html(binlogHtml)
					$("select[name='inventory_groups']").selectpicker('refresh');					
						
				},
			});	
	   }
	   else{
		   $('#deploy_service').attr("disabled",true);
	   }
}

function AssetsTypeSelect(obj,model){ 
	   var index = obj.selectedIndex;
	   var sId = obj.options[index].value; 
	   apply_hosts["hosts"] = []
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
					var sHtml = '';
					for (var i=0; i <response["data"].length; i++){
						apply_hosts["hosts"].push(response["data"][i]["ip"])
						sHtml += '<br>' + response["data"][i]["ip"] 
					};  
					if ( sHtml.length > 0){
		            	new PNotify({
		                    title: "<strong>发现主机:</strong>",
		                    text: sHtml,
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 	
		                 $("#add_task_apply_hosts").val(JSON.stringify(apply_hosts,null, 2))
					}
					else {
		            	new PNotify({
		                    title: "<strong>Ops：</strong>",
		                    text: "该条件下未发现主机资源~",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 	
					}
				
						
				},
			});	
	   }
}

function AssetsSelect(name,dataList,selectIds){
	apply_hosts["hosts"] = []
	if(!selectIds){selectIds=0}
	
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="" disabled>选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		if(dataList[i][name+"_name"]){
			var text = dataList[i][name+"_name"]
		}else if(name=="custom"){
			var text = dataList[i]["detail"]["ip"]	
		}else if(name=="business"){
			var text = dataList[i]["paths"]
		}else if(name=="group"){
			var text = dataList[i]["paths"]
		}
		else{
			var text = dataList[i]["name"]
		}
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

function controlServerSelectHide(value,selectIds){
	if(!selectIds){selectIds=0}
	switch(value)
	   {
		   case "group":
			   $("#group_server").show();
			   $("#custom_server").hide();
			   $("#project_server").hide();
			   $("#inventory_server").hide();
			   $("#tags_server").hide();
			   AssetsSelect("group",requests('get','/api/account/group/'),selectIds)
		       break;
		   case "custom":
			   $("#group_server").hide();
			   $("#custom_server").show();
			   $("#project_server").hide();
			   $("#inventory_server").hide();
			   $("#tags_server").hide();
			   AssetsSelect("custom",requests('get','/api/assets/'),selectIds)
		       break;
		   case "business":
			   $("#group_server").hide();
			   $("#custom_server").hide();
			   $("#project_server").show();
			   $("#inventory_server").hide();
			   $("#tags_server").hide();
			   AssetsSelect("business",requests('get','/api/business/last/'),selectIds)
		       break;		   
		   case "inventory_groups":
			   $("#group_server").hide();
			   $("#custom_server").hide();
			   $("#project_server").hide();
			   $("#inventory_server").show();
			   $("#tags_server").hide();
			   AssetsSelect("inventory",requests('get','/api/inventory/'),selectIds)
			   $("[name='inventory']").trigger("change");
		       break;	
		   case "tags":
			   $("#group_server").hide();
			   $("#custom_server").hide();
			   $("#project_server").hide();
			   $("#inventory_server").hide();
			   $("#tags_server").show();
			   AssetsSelect("tags",requests('get','/api/tags/'),selectIds)
		       break;			   
		   default:
			   $("#group_server").hide();
		   	   $("#custom_server").hide();
		       $("#project_server").hide();
		       $("#inventory_server").hide();
		       $("#tags_server").hide();
	   }
}

var apply_hosts = JSON.parse($("#add_task_apply_hosts").val());

$(document).ready(function() {
	
	$("#server_model").val("");

	$("#server_model").change(function(){
		var obj = document.getElementById("server_model"); 
		var index = obj.selectedIndex;
		var value = obj.options[index].value; 
		controlServerSelectHide(value);	
	});
	
	$("#apply_icon").fileinput({
	 	 maxFileCount: 1,
	     previewFileType: "image",   
	     allowedFileExtensions: ["png", "jpg", "jpeg", "gif"],  //允许的文件后缀
	     previewClass: "bg-warning"
	});	
	
	var apply_config_list = requests("get","/api/apply/config/")["results"]
	var div_str = ''
	for (var i = 0; i < apply_config_list.length; ++i) {
		var random_number = randomNum(1,5)
		var div_tags = '<div class="col-md-4 col-sm-4  profile_details">' +
		                        '<div class="well profile_view">' +
		                          '<div class="col-sm-12">' +
		                            '<h4 class="brief"><i>'+ apply_config_list[i]["apply_name"] +'</i></h4>' +
		                            '<div class="left col-md-7 col-sm-7">' +
		                              '<p><strong>'+ apply_config_list[i]["apply_type"] +'</strong>'+ apply_config_list[i]["apply_desc"] + '</p>' +
		                            '</div>' +
		                            '<div class="right col-md-5 col-sm-5 text-center">' +
		                              '<img src="'+ apply_config_list[i]["apply_icon"] +'" alt="" class="img-circle img-fluid">' +
		                            '</div>' +
		                          '</div>' +
		                          '<div class=" profile-bottom text-center">' +
		                            '<div class=" col-sm-6 emphasis">' +
		                              '<p class="ratings">' +
		                                '<a>'+ random_number +'.0</a>' +
		                                random_star(random_number) +
		                              '</p>' +
		                            '</div>' +
		                            '<div class=" col-sm-6 emphasis">' +
					                    '<div class="btn-group">' +
					                      '<button name="btn-apply-run" class="btn btn-secondary btn-success btn-sm" type="button" value="'+ apply_config_list[i]["id"] +'"><i class="fa fa-play"></i></button>' +
					                      '<button name="btn-apply-edit" class="btn btn-secondary btn-primary btn-sm" type="button" value="'+ apply_config_list[i]["id"] +'"><i class="fa fa-edit"></i></button>' +
					                      '<button name="btn-apply-delete" class="btn btn-secondary btn-danger btn-sm" type="button" value="'+ apply_config_list[i]["id"] +'"><i class="fa fa-times"></i></button>' +
					                    '</div>' +	
		                            '</div>' +
		                          '</div>' +
		                          '<div class="col-sm-12"><p></p></div>' +
		                        '</div>' +
		                      '</div>'
		div_str = div_tags + div_str   
	}
	
	if (div_str.length > 0){
		
		var html_str = '<div class="x_content" id="apply_config_content">' +
							'<div class="col-md-12 col-sm-12  text-center"></div>' +
							'<div class="clearfix"></div>' +
							div_str +
					   '</div>'
		
		$('#apply_config_content').html(html_str)
	}
	
	$("button[name='btn-apply-edit']").on('click', function() {	
    	var vIds = $(this).val();
    	var uri = '/api/apply/config/'+vIds +'/' 
    	var data = requests('get',uri)
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改应用'+ data["apply_name"] +'的数据',
	        content: '<form role="form" method="post" id="apply_config_form" enctype="multipart/form-data">' +
						'<div class="item form-group">' +
							'<label><font color="red">* </font>名称<i class="fa fa-info-circle" data-toggle="tooltip" title="应用名称"></i></label>' +
							'<input class="form-control" name="apply_name" value="'+ data["apply_name"] +'" required>' +
						'</div>' +
						'<div class="item form-group">' +
							'<label><font color="red">* </font>类型<i class="fa fa-info-circle" data-toggle="tooltip" title="应用类型: 比如MySQL、Redis、MongoDB"></i></label>' +
							'<input class="form-control" name="apply_type" value="'+ data["apply_type"] +'" required>' +
						'</div>' +																			
						'<div class="item form-group">' +
							'<label><font color="red">* </font>描述<i class="fa fa-info-circle" data-toggle="tooltip" title="描述应用的作用"></i></label>' +
							'<textarea class="form-control" rows="5"  value="'+ data["apply_desc"] +'" name="apply_desc" required>' + data["apply_desc"] +
							'</textarea>' +
						'</div>' +									
						'<div class="form-group">' +
							'<label><font color="red"> </font>剧本路径<i class="fa fa-info-circle" data-toggle="tooltip" title="应用部署剧本路径"></i></label>' +
							'<input class="form-control" name="apply_playbook"  value="'+ data["apply_playbook"] +'" required>' +					
						'</div>' +										
						'<div class="item form-group">' +
							'<label><font color="red">* </font>变量<i class="fa fa-info-circle" data-toggle="tooltip" title="剧本变量: json格式"></i></label>' +
							'<textarea class="form-control" rows="10" id="apply_payload"  name="apply_payload" required>' + data["apply_payload"] +
							'</textarea>' +		
						'</div>' +			
					'</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	formData = new FormData();
	                    apply_name = this.$content.find("[name='apply_name']").val();
	                    apply_type = this.$content.find("[name='apply_type']").val();
	                    apply_desc = this.$content.find("[name='apply_desc']").val();
	                    apply_playbook = this.$content.find("[name='apply_playbook']").val();
	                    apply_payload = this.$content.find("[name='apply_payload']").val();		                    
						if (apply_payload.replace(/ /g, "").replace(/\t/g, "").length > 0){
							if (isJsonString(apply_payload) == false){
				            	new PNotify({
				                    title: 'Failed!',
				                    text: '变量必须是JSON格式',
				                    type: 'error',
				                    styling: 'bootstrap3'
				                }); 	
								return false;				
							}
						}					
					    formData.append('apply_name',apply_name);
					    formData.append('apply_type',apply_type);
					    formData.append('apply_desc',apply_desc);
					    formData.append('apply_playbook',apply_playbook);	
					    formData.append('apply_payload',apply_payload);	
				    	$.ajax({  
						    processData: false,
						    contentType: false,	
				            type: "PUT",  
				            url:uri,  
				            data:formData,
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
				                    text: '修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				                window.location.reload();
				            }  
				    	});
	                }
	            }
	        }
	    });
    });		
	
    $("button[name='btn-apply-run']").on('click', function() {	
    	var vIds = $(this).val();
    	
    	$("#addApplyTaskSubmit").val(vIds)
    	var uri = '/api/apply/config/'+vIds +'/' 
    	var data = requests('get',uri) 
    	$("#apply_h4").html('<h4 class="modal-title" id="apply_h4"><i class="fa fa-play"></i> 执行<code>'+ data["apply_name"] +'</code>应用部署 <i class="fa fa-spinner"></i></h4>')
    	$('#addApplyTaskModal').modal("show");
    	$("#add_task_apply_payload").val(data["apply_payload"])
    })
    
    $("#addApplyTaskSubmit").on('click', function() {
    	var vIds = $(this).val();
		var server_model = $("#server_model").val();
		var apply_payload = $("#add_task_apply_payload").val()
		var apply_hosts = $("#add_task_apply_hosts").val()
    	formData = new FormData();	     
		if (!isJsonString(apply_payload) && apply_payload.length > 0){
        	new PNotify({
                title: 'Failed!',
                text: '变量必须是JSON格式',
                type: 'error',
                styling: 'bootstrap3'
            }); 	
			return false;				
		}
		
		if (!isJsonString(apply_hosts)){
        	new PNotify({
                title: 'Failed!',
                text: '主机必须是JSON格式',
                type: 'error',
                styling: 'bootstrap3'
            }); 	
			return false;				
		}
		host = jQuery.parseJSON(apply_hosts)
		if (host.hosts.length == 0 && host.hosts instanceof Array){
        	new PNotify({
                title: 'Failed!',
                text: 'hosts字段请输入主机IP',
                type: 'error',
                styling: 'bootstrap3'
            }); 	
			return false;							
		}					
		formData.append('apply_id',vIds);
	    formData.append('apply_hosts',apply_hosts);
	    if (apply_payload.length > 0){
	    	formData.append('apply_payload',apply_payload);	
	    }
    	$.ajax({  
		    processData: false,
		    contentType: false,	
            type: "POST",  
            url:'/api/apply/tasks/',  
            data:formData,
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
		
    });	    
    
//	$("button[name='btn-apply-run']").on('click', function() {	
//    	var vIds = $(this).val();
//    	var uri = '/api/apply/config/'+vIds +'/' 
//    	var data = requests('get',uri)
//	    $.confirm({
//	        icon: 'fa fa-play',
//	        type: 'green',
//	        title: '执行安装【'+ data["apply_name"] + '】应用',
//	        content: '<form role="form" method="post" id="apply_config_form" enctype="multipart/form-data">' +							
//						'<div class="item form-group">' +
//							'<label><font color="red">* </font>自定义主机<i class="fa fa-info-circle" data-toggle="tooltip" title="输入要安装应用的主机"></i></label>' +
//							'<textarea class="form-control" rows="5" name="apply_hosts" required>{\n' + 
//							'    "hosts"'+":"+'[ ]' +
//							'\n}</textarea>' +
//						'</div>' +																		
//						'<div class="item form-group">' +
//							'<label><font color="red">* </font>变量<i class="fa fa-info-circle" data-toggle="tooltip" title="剧本变量: json格式"></i></label>' +
//							'<textarea class="form-control" rows="10" id="apply_payload"  name="apply_payload" required>' + data["apply_payload"] +
//							'</textarea>' +		
//						'</div>' +			
//					'</form>',
//	        buttons: {
//	            '取消': function() {},
//	            '安装': {
//	                btnClass: 'btn-blue',
//	                action: function() {
//	                	formData = new FormData();
//	                    apply_hosts = this.$content.find("[name='apply_hosts']").val();
//	                    apply_payload = this.$content.find("[name='apply_payload']").val();	     
//						if (!isJsonString(apply_payload) && apply_payload.length > 0){
//			            	new PNotify({
//			                    title: 'Failed!',
//			                    text: '变量必须是JSON格式',
//			                    type: 'error',
//			                    styling: 'bootstrap3'
//			                }); 	
//							return false;				
//						}
//						
//						if (!isJsonString(apply_hosts)){
//			            	new PNotify({
//			                    title: 'Failed!',
//			                    text: '主机必须是JSON格式',
//			                    type: 'error',
//			                    styling: 'bootstrap3'
//			                }); 	
//							return false;				
//						}
//						host = jQuery.parseJSON(apply_hosts)
//						if (host.hosts.length == 0 && host.hosts instanceof Array){
//			            	new PNotify({
//			                    title: 'Failed!',
//			                    text: 'hosts字段请输入主机IP',
//			                    type: 'error',
//			                    styling: 'bootstrap3'
//			                }); 	
//							return false;							
//						}					
//						formData.append('apply_id',vIds);
//					    formData.append('apply_hosts',apply_hosts);
//					    if (apply_payload.length > 0){
//					    	formData.append('apply_payload',apply_payload);	
//					    }
//					    
//				    	$.ajax({  
//						    processData: false,
//						    contentType: false,	
//				            type: "POST",  
//				            url:'/api/apply/tasks/',  
//				            data:formData,
//				            error: function(request) {  
//				            	new PNotify({
//				                    title: 'Ops Failed!',
//				                    text: request.responseText,
//				                    type: 'error',
//				                    styling: 'bootstrap3'
//				                });       
//				            },  
//				            success: function(data) {  
//				            	new PNotify({
//				                    title: 'Success!',
//				                    text: '添加成功',
//				                    type: 'success',
//				                    styling: 'bootstrap3'
//				                }); 
////				                window.location.reload();
//				            }  
//				    	});
//	                }
//	            }
//	        }
//	    });
//    });	    
    
	$("button[name='btn-apply-delete']").on('click', function() {	
		var vIds = $(this).val(); 
		uri = '/api/apply/config/'+vIds +'/'
		data = requests('get',uri)
		$.confirm({
		    title: '删除确认',
		    content: "删除【" + data["apply_type"] +"】" + '<strong> <code>' + data["apply_name"] + '</code></strong>应用',
		    type: 'red',
		    buttons: {
		             删除: function () {	
						$.ajax({
							url:'/api/apply/config/'+vIds +'/',
							type:"DELETE",  		
							data:{
								"id":vIds,
							}, 
							success:function(response){
				            	window.location.reload();
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
    
	$("button[name='btn-apply-add']").on('click', function() {	
		var btnObj = $(this);
		var required = ["apply_name","apply_type","apply_desc","apply_icon","apply_playbook"];
	    var formData = new FormData();
		btnObj.attr('disabled',true);
		var form = document.getElementById('apply_config_form');
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
            	btnObj.attr('disabled',false);
				return false;
			}		
		}; 
		if ($('#apply_payload').val().replace(/ /g, "").replace(/\t/g, "").length > 0){
			if (isJsonString($('#apply_payload').val()) == false){
            	new PNotify({
                    title: 'Failed!',
                    text: '变量必须是JSON格式',
                    type: 'error',
                    styling: 'bootstrap3'
                }); 	
            	btnObj.attr('disabled',false);
				return false;				
			}
		}
	    formData.append('apply_name',$('#apply_name').val());
	    formData.append('apply_type',$('#apply_type').val());
	    formData.append('apply_desc',$('#apply_desc').val());
	    formData.append('apply_playbook',$('#apply_playbook').val());	
	    formData.append('apply_payload',$('#apply_payload').val());	
	    formData.append('apply_icon', $("#apply_icon")[0].files[0]);
		$.ajax({
/* 				dataType: "JSON", */
			url:'/api/apply/config/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
            	new PNotify({
                    title: 'Success!',
                    text: '应用添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: '应用添加失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	}) 	
})