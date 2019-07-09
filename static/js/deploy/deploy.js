function isJsonString(str) {
      	try {
            if (typeof JSON.parse(str) == "object") {
                return true;
            }
        } catch(e) {
        }
        return false;
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

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

function DynamicSelect(ids,value){
	$('select[name="'+ids+'"]' +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$('select[name="'+ ids +'"]'+ " option[value='" + value +"']").prop("selected",true);	
	$('select[name="'+ ids +'"]').selectpicker('refresh');
}

function ServicetSelect(projectId,serviceId){
	   if ( projectId > 0){	 
	   		var response = requests('get','/api/project/'+ projectId + '/',{})
			var binlogHtml = '<select class="selectpicker" name="service"  onchange="javascript:AssetsTypeSelect(this,"service");" required><option name="service" value="">请选择业务类型</option>'
			var selectHtml = '';
			for (var i=0; i <response["service_assets"].length; i++){
					if (serviceId == response["service_assets"][i]["id"]){
						selectHtml += '<option selected="selected" name="service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					}else{
						selectHtml += '<option name="service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					}	
			};                        
			binlogHtml =  binlogHtml + selectHtml + '</select>';
			return binlogHtml			
		} 
}

function InventoryGroupsSelect(inventoryId,groupId){
	   if ( inventoryId > 0){
	   		var response = requests('get','/api/inventory/groups/'+ inventoryId + '/',{})
			var binlogHtml = '<select class="form-control" name="deploy_inventory_groups" id="deploy_inventory_groups"   required><option selected="selected" name="deploy_inventory_groups" value="">请选择一个资产组</option>'
			var selectHtml = '';
			for (var i = 0; i < response["data"].length; ++i) {
				if (groupId == response["data"][i]["id"]){
					selectHtml += '<option selected="selected" name="deploy_inventory_groups" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["name"] + '</option>' 	                
				}else{
					selectHtml += '<option name="deploy_inventory_groups" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["name"] + '</option>'
				}						
			}
			binlogHtml =  binlogHtml + selectHtml + '</select>'; 
			return binlogHtml				
		} 
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
		if(dataList[i][name+"_name"]){
			var text = dataList[i][name+"_name"]
		}else if(name=="custom"){
			var text = dataList[i]["detail"]["ip"]+ ' | ' + dataList[i]["project"]+' | '+dataList[i]["service"]			
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
			   AssetsSelect("group",requests('get','/api/group/'),selectIds)
		       break;
		   case "custom":
			   $("#group_server").hide();
			   $("#custom_server").show();
			   $("#project_server").hide();
			   $("#inventory_server").hide();
			   $("#tags_server").hide();
			   AssetsSelect("custom",requests('get','/api/assets/'),selectIds)
		       break;
		   case "service":
			   $("#group_server").hide();
			   $("#custom_server").hide();
			   $("#project_server").show();
			   $("#inventory_server").hide();
			   $("#tags_server").hide();
			   AssetsSelect("project",requests('get','/api/project/'),selectIds)
		       break;		   
		   case "inventory_groups":
			   $("#group_server").hide();
			   $("#custom_server").hide();
			   $("#project_server").hide();
			   $("#inventory_server").show();
			   $("#tags_server").hide();
			   AssetsSelect("inventory",requests('get','/api/inventory/'),selectIds)
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

function format ( data ) {
	var serHtml = '';
	serHtml = "<pre>" + JSON.stringify(data,null,4) + "</pre>";			
    return serHtml;
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
					var binlogHtml = '<select class="selectpicker" name="inventory_groups"  onchange="javascript:AssetsTypeSelect(this,"inventory_groups");" required><option selected="selected"  value="">请选择资产组</option>'
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

function oBtProjectSelect(obj){
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/project/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="service"  onchange="javascript:AssetsTypeSelect(this,"service");" required><option selected="selected" value="">请选择业务类型</option>'
					var selectHtml = '';
					for (var i=0; i <response["service_assets"].length; i++){
						 selectHtml += '<option name="service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("select[name='service']").html(binlogHtml)
					$("select[name='service']").selectpicker('refresh');					
						
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
						sHtml += '<br>' + response["data"][i]["ip"] + " | " + response["data"][i]["project"] + " | " + response["data"][i]["service"]
					};  
					if ( sHtml.length > 0){
		            	new PNotify({
		                    title: "<strong>发现主机:</strong>",
		                    text: sHtml,
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 	
		            	$('#run_ansible_model').removeAttr("disabled");
					}
					else {
		            	new PNotify({
		                    title: "<strong>Ops：</strong>",
		                    text: "该条件下未发现主机资源~",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 	
		            	$('#run_ansible_model').attr("disabled",true);
					}
				
						
				},
			});	
	   }
}

/*function runDeployModel(obj) {
	var btnObj = $(obj);
	btnObj.attr('disabled',true);
	var form = document.getElementById('deployModelRun');
	var post_data = {};
	for (var i = 1; i < form.length; ++i) {
		var name = form[i].name;
		var value = form[i].value;
		var project = name.indexOf("server_model");
		if ( project==0 && value.length==0 && name!="deploy_args"){
        	new PNotify({
                title: 'Warning!',
                text: '请注意必填项不能为空~',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
			btnObj.removeAttr('disabled');
			return false;
		}
	};
	$("#result").html("服务器正在处理，请稍等。。。");
	 轮训获取结果 开始  
    var interval = setInterval(function(){  
        $.ajax({  
            url : '/deploy/run/',  
            type : 'post', 
            data:$('#deployModelRun').serialize(),
            success : function(result){
            	if (result["msg"] !== null ){
            		$("#result").append("<p>"+result["msg"]+"</p>"); 
            		document.getElementById("scrollToTop").scrollIntoView(); 
            		if (result["msg"].indexOf("[Done]") == 0){
            			clearInterval(interval);
        				$.confirm({
        				    title: '执行完成',
        				    content: '',
        				    type: 'blue',
        				    typeAnimated: true,
        				    buttons: {
        				        close: function () {
        				        }
        				    }
        				});	
            			btnObj.removeAttr('disabled');
            		}
            	}
            },
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	    		clearInterval(interval);
	    	}	            
        });  
    },1000); 

	 轮训获取结果结束  
	$.ajax({
		url:'/deploy/model/', 
		type:"POST",  
		data:$('#deployModelRun').serialize(),  
		success:function(response){
			btnObj.removeAttr('disabled');
			if (response["code"] == "500"){
				clearInterval(interval);
				btnObj.removeAttr('disabled');
				$.confirm({
				    title: '执行完成',
				    content: response["msg"],
				    type: 'blue',
				    typeAnimated: true,
				    buttons: {
				        close: function () {
				        }
				    }
				});			
			}
			
		},
    	error:function(response){
    		btnObj.removeAttr('disabled');
    		clearInterval(interval);
			$.confirm({
			    content: "执行失败",
			    type: 'red',
			    typeAnimated: true,
			    buttons: {
			        close: function () {
			        }
			    }
			});
    		
    	}
	})	
}	*/

$(document).ready(function() {
	
	var randromChat = makeRandomId()
	
	if($("#ans_uuid").length){
		$("#ans_uuid").val(uuid())
	}
	
	try
		{
			if($("#inventoryVars").length){
				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/json","ace/theme/terminal");
			}
			else if($("#deployScriptType").length){
		    	var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/sh","ace/theme/terminal");
		    	aceEditAdd.insert("#!/bin/bash");				
			}
			else if($("#deployPlaybookRun").length){
		    	var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/yaml","ace/theme/sqlserver");							
			}
		    if($("#compile-editor-modf").length){
		    	var aceEditModf = setAceEditMode("compile-editor-modf","ace/mode/json","ace/theme/terminal");
		    }   		  
		}
	catch(err)
		{
			console.log(err)
		}
	
	
	$("#server_model").change(function(){
		   var obj = document.getElementById("server_model"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   controlServerSelectHide(value);		   			  
	});
	
	$("#deploy_model").change(function(){
		   var obj = document.getElementById("deploy_model"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   switch(value)
		   {
			   case "raw":
				  $("#deploy_args").val("uptime");	
				  $("#custom_model").hide();
			       break;
			   case "yum":
				   $("#deploy_args").val("name=httpd state=present");
				   $("#custom_model").hide();
			       break;
			   case "service":
				   $("#deploy_args").val("name=mysql state=restarted enabled=yes");
				   $("#custom_model").hide();
			       break;		   
			   case "cron":
				   $("#deploy_args").val('name="sync time" minute=*/3 hour=* day=* month=* weekday=* job="/usr/sbin/ntpdate window.time.com"');
				   $("#custom_model").hide();
			       break;		
			   case "file":
				   $("#deploy_args").val('src=/root/test.txt dest=/tmp/test.txt owner=root group=root mode=700 state=touch');
				   $("#custom_model").hide();
			       break;	
			   case "copy":
				   $("#deploy_args").val('src=/root/test.txt dest=/tmp/test.txt owner=root group=root mode=700 state=touch');
				   $("#custom_model").hide();
			       break;	
			   case "user":
				   $("#deploy_args").val("name=welliam password='$6yshUMNL8dhY'");	
				   $("#custom_model").hide();
			       break;	
			   case "synchronize":
				   $("#deploy_args").val('src=/root/a dest=/tmp/ compress=yes rsync_opts="--exclude=.git --exclude=static/image"');	
				   $("#custom_model").hide();
			       break;	
			   case "get_url":
				   $("#deploy_args").val("url=http://url/test.tar.gz dest=/tmp");
				   $("#custom_model").hide();
			       break;	
			   case "custom":
				   $("#custom_model").show();  
				   $("#deploy_args").val("");
			       break;
			   case "ping":
				   $("#custom_model").hide();;  
				   $("#deploy_args").val("");
			       break;			       
			   default:
				   $("#deploy_args").val("");			   			       
		   }		   
		   			  
	});	
	
    $('#add_inventory_button').click(function(){//点击a标签  
        if($('#add_inventory').is(':hidden')){
        	$('#add_inventory').show();
        }
        else{
        	$('#add_inventory').hide();
        }  
    });	

    $('#deploy_list').click(function(){//点击a标签  
        if($('#add_deploy_tools').is(':hidden')){
        	$('#add_deploy_tools').show();
        	$('#add_deploy_result').show();
        }
        else{
        	$('#add_deploy_tools').hide();
        	$('#add_deploy_result').hide();
        }  
    });    
    
    $('#addInventory').on('click', function () {
		var required = ["inventory_name","inventory_desc"];
	    var formData = new FormData();		
		$(this).attr('disabled',true);
		var form = document.getElementById('inventory');
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
					$(this).removeAttr('disabled');
					return false;
				};					
			};			
		    formData.append('inventory_name',$('#inventory_name').val());
		    formData.append('inventory_desc',$('#inventory_desc').val());
			$.ajax({
	/* 				dataType: "JSON", */
				url:'/deploy/inventory/', //请求地址
				type:"POST",  //提交类似
			    processData: false,
			    contentType: false,				
				data:formData,  //提交参数
				success:function(response){
					$(this).removeAttr('disabled');				
					if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: response["msg"],
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 						
						window.location.reload();
					}
					else {					
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response["msg"],
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
		            	$(this).removeAttr('disabled');
					};
				},
		    	error:function(response){
		    		$(this).removeAttr('disabled');
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: "添加失败",
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
	            	$(this).removeAttr('disabled');
		    	}
			});	
      });        
    
    //new
      if ($("#inventoryListTable").length) {
	    var table = $('#inventoryListTable').DataTable( {
	        "columns": [
	            {
	                "className":      'details-control',
	                "orderable":      false,
	                "data":           null,
	                "defaultContent": ''
	            },
	            { "data": "id" },
	            { "data": "名称" },
	            { "data": "用途描述" },
	            { "data": "添加人" },
	            { "data": "添加日期"},
	            { "data": "操作" }       
	        ],
	        "order": [[2, 'desc']],
			language : {
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
		},	        
	    } );
	     
	    // Add event listener for opening and closing details
	    $('#inventoryListTable tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );
	        aId = row.data()["id"];
	        $.ajax({
	            url : "/api/inventory/"+aId+"/",
	            type : "get",
	            async : false,
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
    };      
    	  
    
	 $('#addInventoryGroups').on('click', function () {	
		var required = ["group_name","inventory"];
		var btnObj = $(this);
		btnObj.attr('disabled',true);
	    var ext_vars = aceEditAdd.getSession().getValue(); 	
	    var formData = new FormData();		
		$(this).attr('disabled',true);
		var form = document.getElementById('inventory_group');
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
			var serverList = new Array();
			$("#server_list option:selected").each(function () {
				serverList.push($(this).val())
			})
			if (serverList.length == 0 ){
	        	new PNotify({
	                title: 'Warning!',
	                text: '请注意必填项不能为空~',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	        	btnObj.removeAttr('disabled');
				return false;			
			}
			var gid = $('#inventoryIds option:selected').val()
		    formData.append('group_name',$('#group_name').val());
		    formData.append('ids',gid);
		    formData.append('server_list',serverList);
		    formData.append('ext_vars',ext_vars);	    	
			$.ajax({
				url:'/api/inventory/groups/' + gid + '/', //请求地址
				type:"POST",  //提交类似
			    processData: false,
			    contentType: false,	
			    async : false,
				data:formData,  //提交参数
				success:function(response){
					btnObj.removeAttr('disabled');		
					if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: response["msg"],
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 	
		            	
						/*window.location.reload();*/ 
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
		    		$(this).attr("disabled",false); 
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: "添加失败",
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 	            	
		    	}
			});	
		});	      

		$('#inventoryListTable tbody').on('click','button[name="btn-inventory-delete"]',function(){
	    	var vIds = $(this).val();
	    	var ip = $("#inventory_"+vIds).text(); 
			$.confirm({
			    title: '删除确认',
			    content: ip,
			    type: 'red',
			    buttons: {
			             删除: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "DELETE",  
			            url:"/api/inventory/" + vIds + '/',  
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
			            	window.location.reload();
			            }  
			    	});
			        },
			           取消: function () {
			            return true;			            
			        },			        
			    }
			});	  	
	    });
	    //new
	    $("#hostLists").change(function(){
	    	id = $('#hostLists option:selected').val()
			$.ajax({
					url:'/api/host/vars/'+ id + '/', 
					type:"GET",  //提交类似
				    processData: false,
				    contentType: false,				
					success:function(response){			
						if (response["code"] == 200){
							document.getElementById('host_vars').value=JSON.stringify(response["data"],null,4);
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
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: "添加失败",
			                    type: 'error',
			                    styling: 'bootstrap3'
			                });
			    	}
				});
	    });	    
		//new
	    $('#addHostVars').click(function(){//点击a标签  
	    	console.log($("#host_vars").val())
			$.ajax({
				url:'/api/host/vars/'+ id + '/', 
				type:"POST",  //提交类似
				contentType: "application/json",
			    data: JSON.stringify({
					'host_vars':$("#host_vars").val()
				}),
				success:function(response){			
					if (response["code"] == 200){
		            	new PNotify({
		                    title: 'Success!',
		                    text: response["msg"],
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
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: "添加失败",
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
		    	}
			});    
	    });		
    	//new
	    $('#deploy_inventory').change(function () {
	 	   var sId = $('#deploy_inventory option:selected').val()
	 	   if ( sId  > 0){	 
	 			$.ajax({
	 				dataType: "JSON",
	 				url: "/api/inventory/groups/" + sId +"/", //请求地址
	 				type:"GET",  //提交类似
	 				success:function(response){
	 					$("#deploy_inventory_groups").empty();
	 					if (response["data"].length){
		 					var selectHtml = '';
		 					var binlogHtml = '<select class="form-control" name="deploy_inventory_groups" id="deploy_inventory_groups"   required><option selected="selected" name="deploy_inventory_groups" value="">请选择一个资产组</option>'
		 					for (var i = 0; i < response["data"].length; ++i) {
								selectHtml += '<option name="deploy_inventory_groups" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["name"] + '</option>' 	                
														
		 					}
		 					binlogHtml =  binlogHtml + selectHtml + '</select>'; 
		 					$("#deploy_inventory_groups").html(binlogHtml);
		 					$('.selectpicker').selectpicker('refresh');		 						
	 					}
	 				},
	 			});	
	 	   }
	 });
	 //new   
	    $('#deploy_inventory_groups').change(function () {
	 	   var sId = $('#deploy_inventory_groups option:selected').val()
	 	   if ( sId  > 0){	 
				$.ajax({
					dataType: "JSON",
					url:'/deploy/inventory/group/' + sId + '/', //请求地址
					type:"GET",  //提交类似
					success:function(response){
						$("#inventory_group_server").empty();
						var binlogHtml = '<select class="selectpicker" id="inventory_group_server" required>'
						var selectHtml = '';
						for (var i=0; i <response["data"].length; i++){
							 if(response["data"][i]["seletcd"] == 1){
							 	selectHtml += '<option name="inventory_group_server" selected="selected" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + " | " + response["data"][i]["project"] + " | " + response["data"][i]["service"] + '</option>' 
							 }else{
							 	selectHtml += '<option name="inventory_group_server"  value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + " | " + response["data"][i]["project"] + " | " + response["data"][i]["service"] + '</option>' 
							 }
							 
						};                        
						binlogHtml =  binlogHtml + selectHtml + '</select>';
						$("#inventory_group_server").html(binlogHtml);	
						$('.selectpicker').selectpicker('refresh');
						if($("#compile-editor-modf").length){
							aceEditModf.setValue(JSON.parse(response["vars"]));	
						}
						
					},
				});	
	 	   }	 	 	   	 	   
	 });
	 //new
	    $('#deploy_inventory_groups_delete').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
	    	var gid = $('#deploy_inventory_groups option:selected').val()
	    	if (gid > 0){
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:"/deploy/inventory/group/" + gid + '/',  
		            data:{
		            	"inventory_group":gid
		            },
		            async: false,  
		            error: function(response) { 
		            	btnObj.removeAttr('disabled');
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: request.responseText,
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
		            },  
		            success: function(response) { 
		            	btnObj.removeAttr('disabled');
						if (response["code"] == 200){
			            	new PNotify({
			                    title: 'Success!',
			                    text: response["msg"],
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
//		            	window.location.reload();
		            }  
		    	}); 
	    	} 	
	    });	 
	    
	    $('#modfInventoryGroup').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
	    	var gid = $('#deploy_inventory_groups option:selected').val()
	    	if (gid > 0){
	    		var ext_vars = aceEditModf.getSession().getValue(); 
				var serverList = new Array();
				$("#inventory_group_server option:selected").each(function () {
					serverList.push($(this).val())
				});	    		
		    	$.ajax({  
		            type: "PUT",  
		            url:"/deploy/inventory/group/" + gid + '/',  
		            data:{
		            	"sList":serverList,
		            	'ext_vars':ext_vars
		            },
		            async: false,  
		            error: function(response) { 
		            	btnObj.removeAttr('disabled');
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });   		            	
		            },  
		            success: function(response) {  
		            	btnObj.removeAttr('disabled');
						if (response["code"] == 200){
			            	new PNotify({
			                    title: 'Success!',
			                    text: response["msg"],
			                    type: 'success',
			                    styling: 'bootstrap3'
			                });
//			            	window.location.reload();			            	
						}
						
						else {
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: response["msg"],
			                    type: 'error',
			                    styling: 'bootstrap3'
			                }); 
						};	
		            }  
		    	}); 	    		
	    	} 	
	    });	
	    //new
	    if($("#deployScriptType").length){
		    $("button[name='btn-deploy-scripts']").on('click', function() {
		    	var model = $(this).val();
		    	switch(model)
		    		{
		    			case "sh":
		    				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/" + model,"ace/theme/terminal");	 
		    				aceEditAdd.insert("#!/bin/bash");
		    				break;
		    			case "python":
		    				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/" + model,"ace/theme/terminal");
		    				aceEditAdd.insert("#!/usr/bin/python");
		    				break;
		    			case "perl":
		    				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/" + model,"ace/theme/terminal");
		    				aceEditAdd.insert("#!/usr/bin/perl");
		    				break;		   		       
		    			default:
		    				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/sh","ace/theme/terminal");
		    				aceEditAdd.insert("#!/bin/bash");	       
		    		}		    	
		    });	    	
	    }
	  //new
	    $('#save_deploy_script').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
			var form = document.getElementById('deployScriptRun');
		    var contents = aceEditAdd.getSession().getValue(); 
		    var script_name = document.getElementById("script_name").value;
		    if ( contents.length == 0 || script_name.length == 0){
	        	new PNotify({
	                title: 'Warning!',
	                text: '脚本内容与名称不能为空',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
		    	btnObj.removeAttr('disabled');
		    	return false;
		    };		
			var ansible_server = new Array();
			$("select[name='custom'] option:selected").each(function(){
				ansible_server.push($(this).val());
	        });
//	 	    /* 轮训获取结果结束  */
			$.ajax({
				url:'/deploy/scripts/', //请求地址
				type:"POST",  //提交类似
				data:{
					'script_name':$("#script_name").val(),
					'server_model':$('#server_model option:selected').val(),
					'service':$('select[name="service"] option:selected').val(),
					'group':$('select[name="group"] option:selected').val(),
					'tags':$('select[name="tags"] option:selected').val(),
					'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
					'script_args':$("#script_args").val(),
					'script_file':contents,
					'debug':$('#deploy_debug option:selected').val(),
					'server':ansible_server
				},//$('#deployModelRun').serialize() + '&script_file=' + contents,  //不能是被脚本里面的&&符号
				success:function(response){
					btnObj.removeAttr('disabled');
					if (response["code"] == "500"){
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response["msg"],
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
					}
					else{
		            	window.location.reload();	                				
					}
					
				},
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: "保存失败",
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
		    	}
			})	    	
	    })  
	    
	    $('#run_deploy_model').on('click',function(){
    		var btnObj = $(this);
    		btnObj.attr('disabled',true);
    		var form = document.getElementById('deployModelRun');
    		var post_data = {};
    		for (var i = 1; i < form.length; ++i) {
    			var name = form[i].name;
    			var value = form[i].value;
    			var project = name.indexOf("server_model");
    			if ( project==0 && value.length==0 && name!="deploy_args"){
    	        	new PNotify({
    	                title: 'Warning!',
    	                text: '请注意必填项不能为空~',
    	                type: 'warning',
    	                styling: 'bootstrap3'
    	            }); 
    				btnObj.removeAttr('disabled');
    				return false;
    			}
    		};
    	    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    	    let websocket = new WebSocket(ws_scheme + '://' + window.location.host + "/ws/ansible/model/" + randromChat + '/');
    	    let out_print = $("#result");

    	    websocket.onopen = function () {
    	    	out_print.html('服务器正在处理，请稍等。。。\n\n');
    	    	websocket.send(JSON.stringify($('#deployModelRun').serializeObject()));
    	    };

    	    websocket.onmessage = function (event) {
    	    	out_print.append(event.data+'\n')
    	    };

    	    websocket.onerror = function(event) {
    	    	console.log(event)
    	    	websocket.close();
    	    };    
    	    
    	    websocket.onclose = function () {
    	    	btnObj.removeAttr('disabled');
    	    }		    		    	
	    })
	    //new
//	    $('#run_deploy_script').on('click', function() {
//			var btnObj = $(this);
//			btnObj.attr('disabled',true);
//			var form = document.getElementById('deployScriptRun');
//		    var contents = aceEditAdd.getSession().getValue(); 
//		    var script_name = document.getElementById("script_name").value;
//		    if ( contents.length == 0 || script_name.length == 0){
//	        	new PNotify({
//	                title: 'Warning!',
//	                text: '脚本内容与名称不能为空',
//	                type: 'warning',
//	                styling: 'bootstrap3'
//	            }); 
//		    	btnObj.removeAttr('disabled');
//		    	return false;
//		    };	
//		    $("#result").html("服务器正在处理，请稍等。。。\n");
//			var ansible_server = new Array();
//			$("select[name='custom'] option:selected").each(function(){
//				ansible_server.push($(this).val());
//	        });
//			/* 轮训获取结果 开始  */
//	 	   var interval = setInterval(function(){  
//		        $.ajax({  
//		            url : '/deploy/run/',  
//		            type : 'post', 
//		            data:$('#deployScriptRun').serialize(),
//		            success : function(result){
//		            	if (result["msg"] !== null ){
//		            		$("#result").append("<p>"+result["msg"]+"</p>"); 
//		            		document.getElementById("scrollToTop").scrollIntoView(); 
//		            		if (result["msg"].indexOf("[Done]") == 0){
//		            			clearInterval(interval);
//		            			btnObj.removeAttr('disabled');
//		        				$.confirm({
//		        				    title: '执行完成',
//		        				    content: '',
//		        				    type: 'blue',
//		        				    typeAnimated: true,
//		        				    buttons: {
//		        				        close: function () {
//		        				        }
//		        				    }
//		        				});			            			
//		            		}
//		            	}
//		            },
//			    	error:function(response){
//			    		btnObj.removeAttr('disabled');
//			    		clearInterval(interval);
//			    	}	            
//		        });  
//		    },1000); 			
////	 	    /* 轮训获取结果结束  */
//			$.ajax({
//				url:'/deploy/scripts/run/', //请求地址
//				type:"POST",  //提交类似
//				data:{
//					'script_name':$("#script_name").val(),
//					'server_model':$('#server_model option:selected').val(),
//					'service':$('select[name="service"] option:selected').val(),
//					'group':$('select[name="group"] option:selected').val(),
//					'tags':$('select[name="tags"] option:selected').val(),
//					'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
//					'script_args':$("#script_args").val(),
//					'ans_uuid':$("#ans_uuid").val(),
//					'script_file':contents,
//					'debug':$('#deploy_debug option:selected').val(),
//					'server':ansible_server
//				},//$('#deployModelRun').serialize() + '&script_file=' + contents,  //不能是被脚本里面的&&符号
//				success:function(response){
//					btnObj.removeAttr('disabled');
//					if (response["code"] == "500"){
//						clearInterval(interval);
//						btnObj.removeAttr('disabled');
//		            	new PNotify({
//		                    title: 'Ops Failed!',
//		                    text: "执行失败",
//		                    type: 'error',
//		                    styling: 'bootstrap3'
//		                }); 
//					}					
//				},
//		    	error:function(response){
//		    		btnObj.removeAttr('disabled');
//		    		clearInterval(interval);
//		    	}
//			})	    	
//	    }) 
	    
	    $('#run_deploy_script').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
			var form = document.getElementById('deployScriptRun');
		    var contents = aceEditAdd.getSession().getValue(); 
		    var script_name = document.getElementById("script_name").value;
		    if ( contents.length == 0 || script_name.length == 0){
	        	new PNotify({
	                title: 'Warning!',
	                text: '脚本内容与名称不能为空',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
		    	btnObj.removeAttr('disabled');
		    	return false;
		    };	
		    $("#result").html("服务器正在处理，请稍等。。。\n");
			var ansible_server = new Array();
			$("select[name='custom'] option:selected").each(function(){
				ansible_server.push($(this).val());
	        });
			
		    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
		    let websocket = new WebSocket(ws_scheme + '://' + window.location.host + "/ws/ansible/script/" + randromChat + '/');
		    let out_print = $("#result");
		    
		    websocket.onopen = function () {
		    	out_print.html('服务器正在处理，请稍等。。。\n\n');
		    	let data = {
					'script_name':$("#script_name").val(),
					'server_model':$('#server_model option:selected').val(),
					'service':$('select[name="service"] option:selected').val(),
					'group':$('select[name="group"] option:selected').val(),
					'tags':$('select[name="tags"] option:selected').val(),
					'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
					'script_args':$("#script_args").val(),
					'ans_uuid':$("#ans_uuid").val(),
					'script_file':contents,
					'debug':$('#deploy_debug option:selected').val(),
					'custom':ansible_server
				}
		    	websocket.send(JSON.stringify(data));
		    };

		    websocket.onmessage = function (event) {
		    	out_print.append(event.data+'\n')
		    };

		    websocket.onerror = function(event) {
		    	console.log(event)
		    	websocket.close();
		    };    
		    
		    websocket.onclose = function () {
		    	btnObj.removeAttr('disabled');
		    }			    
		        	
	    }) 
	    
	  //new
      if ($("#deployScriptsList").length) {
	    var table = $('#deployScriptsList').DataTable( {
	        "order": [[5, 'desc']],
			language : {
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
		},	        
	    });	
	  }  
	  //new
	  $("button[name='btn-script-edit']").on("click", function(){
	    $('#add_deploy_tools').show();
	    $('#add_deploy_result').show();			  
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
	  	var vIds = $(this).val();
        $.ajax({  
            url : '/deploy/scripts/?sid='+ vIds ,  
            type : 'get', 
            success : function(response){
            	btnObj.removeAttr('disabled');
            	if(response["code"] == "200"){
            		var script = JSON.parse(response["data"])         		
            		$("#script_name").val(script["script_name"]).attr('disabled',true);	 
					aceEditAdd.setValue(script["script_contents"]);
					//修改动态主机
					DynamicSelect("server_model",script["script_type"])	
					if (script["script_type"]=="group"){
						controlServerSelectHide(script["script_type"],script["script_group"]);
					}	
					if (script["script_type"]=="tags"){
						controlServerSelectHide(script["script_type"],script["script_tags"]);
					}					
					else if(script["script_type"]=="service"){
						var porject = requests('get','/api/service/'+ script["script_service"] + '/');						
						$("select[name='porject'] option[value='" + porject["project_id"] +"']").attr("selected",true);
						$("select[name='service']").html(ServicetSelect(porject["project_id"],script["script_service"]));						
						controlServerSelectHide(script["script_type"],porject["project_id"]);
	
					}
					else if(script["script_type"]=="custom"){
						controlServerSelectHide(script["script_type"]);
						for (var i = 0; i < script["script_server"].length; ++i) {
							$("select[name='custom'] option[value='" + script["script_server"][i] +"']").attr("selected",true);
						}			
					}
					else if(script["script_type"]=="inventory_groups"){
						controlServerSelectHide(script["script_type"]);
						var inventory = requests('get','/api/inventory/groups/query/'+ script["script_inventory_groups"] + '/');
						$("select[name='inventory'] option[value='" + inventory["inventory_id"] +"']").attr("selected",true);
						$("select[name='inventory_groups']").html(InventoryGroupsSelect(inventory["inventory_id"],script["script_inventory_groups"]));
						
					}
					$('.selectpicker').selectpicker('refresh');
					$("#script_args").val(script["script_args"]);	
			   		$("#save_deploy_script").hide();
			   		$("#modf_deploy_script").show();	
			   		$("#modf_deploy_script").val(vIds);
            	}
            	
            },
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	    	}	            
        });		
	  });
	  //new
	  $("#modf_deploy_script").on("click", function(){	  
    	  if($("#modf_deploy_script").val().length){
    			var btnObj = $(this);
    			btnObj.attr('disabled',true);
    		    var contents = aceEditAdd.getSession().getValue(); 
    		    var script_name = document.getElementById("script_name").value;
    		    if ( contents.length == 0 || script_name.length == 0){
    	        	new PNotify({
    	                title: 'Warning!',
    	                text: '脚本内容与名称不能为空',
    	                type: 'warning',
    	                styling: 'bootstrap3'
    	            }); 
    		    	btnObj.removeAttr('disabled');
    		    	return false;
    		    }; 
    			var ansible_server = new Array();
    			$("select[name='custom'] option:selected").each(function(){
    				ansible_server.push($(this).val());
    	        });			
    		  	var vIds = $(this).val();
	  			$.ajax({
					url:'/deploy/scripts/', //请求地址
					type:"PUT",  //提交类似
					data:{
						'script_id':vIds,
						'server_model':$('#server_model option:selected').val(),
						'service':$('select[name="service"] option:selected').val(),
						'group':$('select[name="group"] option:selected').val(),
						'tags':$('select[name="tags"] option:selected').val(),
						'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),						
						'script_args':$("#script_args").val(),
						'script_file':contents,
						'server':ansible_server
					},
					success:function(response){
						btnObj.removeAttr('disabled');
						if (response["code"] == "200"){
			            	new PNotify({
			                    title: 'Success!',
			                    text: response["msg"],
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
					},
			    	error:function(response){
			    		btnObj.removeAttr('disabled');
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "保存失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
			    	}
				})	    		  
    	  }else{
				$.confirm({
				    title: '脚本编辑',
				    content: '请先选择部署脚本',
				    type: 'red',
				    typeAnimated: true,
				    buttons: {
				        close: function () {
				        }
				    }
				});	    		  
    	  }
  	  });
	  //new
	  $("button[name='btn-script-delete']").on("click", function(){		  
			var btnObj = $(this);
			btnObj.attr('disabled',true);		  
		  	var vIds = $(this).val();
	    	var text = $("#script_"+vIds).text(); 
			$.confirm({
			    title: '删除确认',
			    content: text,
			    type: 'red',
			    buttons: {
			        删除: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "DELETE",  
			            url:'/deploy/scripts/',
			            data:{
			            	"script_id":vIds
			            },
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
			                    text: response["msg"],
			                    type: 'success',
			                    styling: 'bootstrap3'
			                });	
			            	window.location.reload();
			            }  
			    	});
			        },
			        取消: function () {
			            return true;			            
			        },			        
			    }
			});		        
	  });
	  //deploy_playbook
      if ($("#deployPlaybookList").length) {
  	    var table = $('#deployPlaybookList').DataTable( {
  	        "order": [[5, 'desc']],
			language : {
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
		},  	        
  	    });	
  	  };
	  $('#save_deploy_playbook').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
			var form = document.getElementById('deployPlaybookRun');
		    var contents = aceEditAdd.getSession().getValue(); 
		    let server_model = $('#server_model option:selected').val()
		    var playbook_name = document.getElementById("playbook_name").value;
		    if ( contents.length == 0 || playbook_name.length == 0 || server_model.length == 0 ){
	        	new PNotify({
	                title: 'Warning!',
	                text: '剧本内容与名称或者服务器不能为空',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
		    	btnObj.removeAttr('disabled');
		    	return false;
		    };		
			var ansible_server = new Array();
			$("select[name='custom'] option:selected").each(function(){
				ansible_server.push($(this).val());
	        });
			if ($("#playbook_vars").val().length && isJsonString($("#playbook_vars").val()) == false){
	        	new PNotify({
	                title: 'Warning!',
	                text: '外部变量需要为json格式',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
		    	btnObj.removeAttr('disabled');
		    	return false;	        	
			}
//	 	    /* 轮训获取结果结束  */
			$.ajax({
				url:'/deploy/playbook/', //请求地址
				type:"POST",  //提交类似
				data:{
					'playbook_name':$("#playbook_name").val(),
					'playbook_desc':$("#playbook_desc").val(),
					'server_model':server_model,
					'service':$('select[name="service"] option:selected').val(),
					'group':$('select[name="group"] option:selected').val(),
					'tags':$('select[name="tags"] option:selected').val(),
					'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
					'playbook_file':contents,
					'server':ansible_server,
					'playbook_vars':$("#playbook_vars").val(),
				},
				success:function(response){
					btnObj.removeAttr('disabled');
					if (response["code"] == "500"){
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: response["msg"],
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
					}
					else{
		            	window.location.reload();	                				
					}
					
				},
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: "保存失败",
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
		    	}
			})	    	
	    });
	  //new
	  $("button[name='btn-playbook-edit']").on("click", function(){
	    $('#add_deploy_tools').show();
	    $('#add_deploy_result').show();			  
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
	  	var vIds = $(this).val();
        $.ajax({  
            url : '/deploy/playbook/?pid='+ vIds ,  
            type : 'get', 
            success : function(response){
            	btnObj.removeAttr('disabled');
            	if(response["code"] == "200"){
            		var playbook = JSON.parse(response["data"])         		
            		$("#playbook_name").val(playbook["playbook_name"]).attr('disabled',true); 
					aceEditAdd.setValue(playbook["playbook_contents"]);
					DynamicSelect("server_model",playbook["playbook_type"]);	
					if (playbook["playbook_type"]=="group"){
						controlServerSelectHide(playbook["playbook_type"],playbook["playbook_group"]);
					}    
					if (playbook["playbook_type"]=="tags"){
						controlServerSelectHide(playbook["playbook_type"],playbook["playbook_tags"]);
					} 					
					else if(playbook["playbook_type"]=="service"){
						var porject = requests('get','/api/service/'+ playbook["playbook_service"] + '/');
						$("select[name='porject'] option[value='" + porject["project_id"] +"']").attr("selected",true);
						$("select[name='service']").html(ServicetSelect(porject["project_id"],playbook["playbook_service"]));	
						controlServerSelectHide(playbook["playbook_type"],porject["project_id"]);
					}
					else if(playbook["playbook_type"]=="custom"){
						controlServerSelectHide(playbook["playbook_type"]);
						for (var i = 0; i < playbook["playbook_server"].length; ++i) {
							$("select[name='custom'] option[value='" + playbook["playbook_server"][i] +"']").attr("selected",true);
						}					
					}					
					else if(playbook["playbook_type"]=="inventory_groups"){
						controlServerSelectHide(playbook["playbook_type"])
						var inventory = requests('get','/api/inventory/groups/query/'+ playbook["playbook_inventory_groups"] + '/');
						$("select[name='inventory'] option[value='" + inventory["inventory_id"] +"']").attr("selected",true);
						$("select[name='inventory_groups']").html(InventoryGroupsSelect(inventory["inventory_id"],playbook["playbook_inventory_groups"]));
					}
					$('.selectpicker').selectpicker('refresh');	
					$("#playbook_vars").val(playbook["playbook_vars"]);	
					$("#playbook_desc").val(playbook["playbook_desc"]);	
			   		$("#save_deploy_playbook").hide();
			   		$("#modf_deploy_playbook").show();	
			   		$("#modf_deploy_playbook").val(vIds);
			   		$("#run_deploy_playbook").val(vIds);
            	}
            	
            },
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	    	}	            
        });		
	  });
	  //new
	  $("#modf_deploy_playbook").on("click", function(){	  
    	  if($("#modf_deploy_playbook").val().length){
    			var btnObj = $(this);
    			btnObj.attr('disabled',true);
    		    var contents = aceEditAdd.getSession().getValue(); 
    		    let server_model = $('#server_model option:selected').val()
    		    var playbook_name = document.getElementById("playbook_name").value;
    		    if ( contents.length == 0 || playbook_name.length == 0 || server_model.length == 0){
    	        	new PNotify({
    	                title: 'Warning!',
    	                text: '剧本内容与名称或者服务器不能为空',
    	                type: 'warning',
    	                styling: 'bootstrap3'
    	            }); 
    		    	btnObj.removeAttr('disabled');
    		    	return false;
    		    }; 
    			var ansible_server = new Array();
    			$("select[name='custom'] option:selected").each(function(){
    				ansible_server.push($(this).val());
    	        }); 			
    		  	var vIds = $(this).val();
	  			$.ajax({
					url:'/deploy/playbook/', //请求地址
					dataType: "json",
					type:"PUT",  //提交类似
					data:{
						'playbook_id':vIds,
						'playbook_desc':$("#playbook_desc").val(),
						'server_model':server_model,
						'service':$('select[name="service"] option:selected').val(),
						'group':$('select[name="group"] option:selected').val(),
						'tags':$('select[name="tags"] option:selected').val(),
						'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
						'playbook_file':contents,
						'server':ansible_server,
						'playbook_vars':$("#playbook_vars").val(),
					},
					success:function(response){
						btnObj.removeAttr('disabled');
						if (response["code"] == "200"){
			            	new PNotify({
			                    title: 'Success!',
			                    text: response["msg"],
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
					},
			    	error:function(response){
			    		btnObj.removeAttr('disabled');
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "保存失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 
			    	}
				})	    		  
    	  }else{
				$.confirm({
				    title: '剧本编辑',
				    content: '请先选择部署剧本',
				    type: 'red',
				    typeAnimated: true,
				    buttons: {
				        close: function () {
				        }
				    }
				});	    		  
    	  }
  	  });
	  

	  $('#run_deploy_playbook').on('click', function() {
			var btnObj = $(this);
			btnObj.attr('disabled',true);
			var vIds = $(this).val();
			let server_model = $('#server_model option:selected').val()
			if (vIds){
				var form = document.getElementById('deployPlaybookRun');
			    var contents = aceEditAdd.getSession().getValue(); 
			    var playbook_name = document.getElementById("playbook_name").value;
			    if ( contents.length == 0 || playbook_name.length == 0 || server_model.length == 0){
		        	new PNotify({
		                title: 'Warning!',
		                text: '剧本内容与名称或者服务器不能为空',
		                type: 'warning',
		                styling: 'bootstrap3'
		            }); 
			    	btnObj.removeAttr('disabled');
			    	return false;
			    };	
			    $("#result").html("服务器正在处理，请稍等。。。");
				var ansible_server = new Array();
				$("#deploy_server option:selected").each(function(){
					ansible_server.push($(this).val());
		        });
				
			    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
			    let websocket = new WebSocket(ws_scheme + '://' + window.location.host + "/ws/ansible/playbook/" + randromChat + '/');
			    let out_print = $("#result");
			    
			    websocket.onopen = function () {
			    	out_print.html('服务器正在处理，请稍等。。。\n\n');
			    	let data = {
							'playbook_id':$("#run_deploy_playbook").val(),
							'server_model':$('#server_model option:selected').val(),
							'service':$('select[name="service"] option:selected').val(),
							'group':$('select[name="group"] option:selected').val(),
							'tags':$('select[name="tags"] option:selected').val(),
							'inventory_groups':$('select[name="inventory_groups"] option:selected').val(),
							'playbook_file':contents,
							'custom':ansible_server,
							'ans_uuid':$("#ans_uuid").val(),
							'playbook_vars':$("#playbook_vars").val(),	
					}
			    	websocket.send(JSON.stringify(data));
			    };
	
			    websocket.onmessage = function (event) {
			    	out_print.append(event.data+'\n')
			    };
	
			    websocket.onerror = function(event) {
			    	console.log(event)
			    	websocket.close();
			    };    
			    
			    websocket.onclose = function () {
			    	btnObj.removeAttr('disabled');
			    }				
  				
			}else{
				btnObj.removeAttr('disabled');
				$.confirm({
				    title: '运行剧本',
				    content: '请先选择部署剧本',
				    type: 'red',
				    typeAnimated: true,
				    buttons: {
				        close: function () {
				        }
				    }
				});	 				
			}				
	    });	  
	  
	  //new
//	  $('#run_deploy_playbook').on('click', function() {
//			var btnObj = $(this);
//			btnObj.attr('disabled',true);
//			var vIds = $(this).val();
//			if (vIds){
//				var form = document.getElementById('deployPlaybookRun');
//			    var contents = aceEditAdd.getSession().getValue(); 
//			    var playbook_name = document.getElementById("playbook_name").value;
//			    if ( contents.length == 0 || playbook_name.length == 0){
//		        	new PNotify({
//		                title: 'Warning!',
//		                text: '脚本内容与名称不能为空',
//		                type: 'warning',
//		                styling: 'bootstrap3'
//		            }); 
//			    	btnObj.removeAttr('disabled');
//			    	return false;
//			    };	
//			    $("#result").html("服务器正在处理，请稍等。。。");
//				var ansible_server = new Array();
//				$("#deploy_server option:selected").each(function(){
//					ansible_server.push($(this).val());
//		        });
//				/* 轮训获取结果 开始  */
//		 	    var interval = setInterval(function(){  
//			        $.ajax({  
//			            url : '/deploy/run/',  
//			            type : 'post', 
//			            data:$('#deployPlaybookRun').serialize(),
//			            success : function(result){
//			            	if (result["msg"] !== null ){
//			            		$("#result").append("<p>"+result["msg"]+"</p>"); 
//			            		document.getElementById("scrollToTop").scrollIntoView(); 
//			            		if (result["msg"].indexOf("[Done]") == 0){
//			            			clearInterval(interval);
//			            			btnObj.removeAttr('disabled');
//			        				$.confirm({
//			        				    title: '执行完成',
//			        				    content: '',
//			        				    type: 'blue',
//			        				    typeAnimated: true,
//			        				    buttons: {
//			        				        close: function () {
//			        				        }
//			        				    }
//			        				});			            			
//			            		}
//			            	}
//			            },
//				    	error:function(response){
//				    		btnObj.removeAttr('disabled');
//				    		clearInterval(interval);
//				    	}	            
//			        });  
//			    },1000); 			
////			 	    /* 轮训获取结果结束  */
//				$.ajax({
//					url:'/deploy/playbook/run/', //请求地址
//					type:"POST",  //提交类似
//					data:{
//						'playbook_id':$("#run_deploy_playbook").val(),
//						'service':$('#deploy_service option:selected').val(),
//						'group':$('#deploy_group option:selected').val(),
//						'tags':$('select[name="tags"] option:selected').val(),
//						'inventory_groups':$('#deploy_inventory_groups option:selected').val(),
//						'playbook_file':contents,
//						'server':ansible_server,
//						'ans_uuid':$("#ans_uuid").val(),
//						'playbook_vars':$("#playbook_vars").val(),						
//					},
//					success:function(response){
//						btnObj.removeAttr('disabled');
//						if (response["code"] == "500"){
//							clearInterval(interval);
//							btnObj.removeAttr('disabled');
//			            	new PNotify({
//			                    title: 'Ops Failed!',
//			                    text: "保存失败",
//			                    type: 'error',
//			                    styling: 'bootstrap3'
//			                }); 
//						}					
//					},
//			    	error:function(response){
//			    		btnObj.removeAttr('disabled');
//			    		clearInterval(interval);
//			    	}
//				})	  				
//			}else{
//				btnObj.removeAttr('disabled');
//				$.confirm({
//				    title: '运行剧本',
//				    content: '请先选择部署剧本',
//				    type: 'red',
//				    typeAnimated: true,
//				    buttons: {
//				        close: function () {
//				        }
//				    }
//				});	 				
//			}				
//	    });
	  //new
	  $("button[name='btn-playbook-delete']").on("click", function(){		  
			var btnObj = $(this);
			btnObj.attr('disabled',true);		  
		  	var vIds = $(this).val();
	    	var text = $("#playbook_"+vIds).text(); 
			$.confirm({
			    title: '删除确认',
			    content: text,
			    type: 'red',
			    buttons: {
			        删除: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "DELETE",  
			            url:'/deploy/playbook/',
			            data:{
			            	"playbook_id":vIds
			            },
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
			                    text: response["msg"],
			                    type: 'success',
			                    styling: 'bootstrap3'
			                });	
			            	window.location.reload();
			            }  
			    	});
			        },
			        取消: function () {
			            return true;			            
			        },			        
			    }
			});		        
	  });	  
	    
}); 

