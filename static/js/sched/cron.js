function isJsonString(str) {
      	try {
            if (typeof JSON.parse(str) == "object") {
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

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
}

function ServicetSelect(projectId,serviceId){
	   if ( projectId > 0){	 
	   		var response = requests('get','/api/project/'+ projectId + '/',{})
			var binlogHtml = '<select class="selectpicker" name="deploy_service" id="deploy_service" onchange="javascript:AssetsTypeSelect();" required><option selected="selected" name="deploy_service" value="">请选择业务类型</option>'
			var selectHtml = '';
			for (var i=0; i <response["service_assets"].length; i++){
					if (serviceId == response["service_assets"][i]["id"]){
						selectHtml += '<option selected="selected" name="deploy_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					}else{
						selectHtml += '<option name="deploy_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
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



function controlScriptHide(value){
	switch(value)
	{
		case "online":
			$('#uploadScript').hide();
			$('#onlineScript').show();
			$('#scriptPath').show();
			break;
		case "upload":
			$('#onlineScript').hide();
			$('#uploadScript').show();	    				
			$('#scriptPath').show();
			break;
		case "command":
			$('#onlineScript').hide();
			$('#uploadScript').hide();	    				
			$('#scriptPath').hide();
			break;	    				
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


	

$(document).ready(function() {	
	try
		{
			if($("#inventoryVars").length){
				var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/json","ace/theme/terminal");
			}
			else if($("#deployPlaybookRun").length){
		    	var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/yaml","ace/theme/sqlserver");							
			}
			else if($("#cronbScriptType").length){
		    	var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/sh","ace/theme/terminal");
		    	aceEditAdd.insert("#!/bin/bash");
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
	
	if($("#deploy_server").length){
		var dataList = requests('get','/api/assets/')
		AssetsSelect("deploy_server",dataList)
	}

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
	   
    function InitDataTable(tableId)
    {
      oOverviewTable =$('#'+tableId).dataTable(
    		  {
    			    "dom": "Bfrtip",
    	    		"bScrollCollapse": false, 				
    	    	    "bRetrieve": true,			
    	    		"destroy": true, 
    	    		"buttons" : [{
    	                text: '<span class="fa fa-plus"></span>',
    	                className: "btn-xs",
    	                action: function ( e, dt, node, config ) {
    	                    if($('#add_deploy_tools').is(':hidden')){
    	                    	$('#add_deploy_tools').show();
    	                    	$('#add_deploy_result').show();
    	                    }
    	                    else{
    	                    	$('#add_deploy_tools').hide();
    	                    	$('#add_deploy_result').hide();
    	                    } 
    	                }
    	            }],    	    		
    	    		"data":	requests('get','/api/sched/cron/'),
    	    		columns:[
    	    	                {"data": "id"},
    	    	                {"data": "cron_name"},
    	    	                {"data": "crontab_server"},		                
    	    	                {"data": "cron_minute"},
    	    	                {"data": "cron_hour"},
    	    	                {"data": "cron_day"},
    	    	                {"data": "cron_week"},
    	    	                {"data": "cron_month"},	                	                	            
    	    	                {"data": "cron_command"},	
    	    	                {"data": "cron_status"},				                
    	    		  ],
    	    		 columnDefs : [
    	    				{
    	    					targets: [9],
    	    					render: function(data, type, row, meta) {
    	    						if(row.cron_status == 2){
    	    							return '<span class="label label-danger">禁用</span>'
    	    						}else if(row.cron_status == 1){
    	    							return '<span class="label label-success">启用</span'
    	    						}else{
    	    							return '<span class="label label-warning">失败</span>'
    	    						}
    	    					},
    	    					"className": "text-center",
    	    				},						               
    	    		        {
    	    				targets: [10],
    	    				render: function(data, type, row, meta) {
    	    					if(row.cron_status == 2){
    	    						var disable = '<button type="button" name="btn-script-enable" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-thumbs-o-up" aria-hidden="true"></span></button>'
    	    					}else if(row.cron_status == 1){
    	    						var disable = '<button type="button" name="btn-script-disabled" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-thumbs-o-down" aria-hidden="true"></span></button>'
    	    					}
    	                        return '<div class="btn-group  btn-group-xs">' +	
    	                           '<button type="button" name="btn-script-edit" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-pencil-square-o" aria-hidden="true"></span>' +	
    	                           '</button>' + disable +			                				                            		                            			                          
    	                           '<button type="button" name="btn-script-view" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
    	                           '</button>' +	
    	                           '<button type="button" name="btn-script-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
    	                           '</button>' +			                            
    	                          '</div>';
    	    				},
    	    				"className": "text-center",
    	    			}],			  
    	    		  /*国际化语言*/
    	    		  language : {
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
    	    			},
    	    			
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

    function AutoReload()
    {
      RefreshTable('#crontabList', '/api/sched/cron/');
      setTimeout(function(){AutoReload();}, 30000);
    }
    
    //初始化表格
    InitDataTable('crontabList');
    //每隔30秒刷新table
//    setTimeout(function(){AutoReload();}, 30000);

    
    cron_type = 'command'
    if($("#cronbScriptType").length){
	    $("button[name='btn-cron-scripts']").on('click', function() {
	    	cron_type = $(this).val();
	    	controlScriptHide(cron_type);	    	
	    });	    	
    }
    
    $('#add_crontab').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);
		var required = ["cron_minute","cron_hour","cron_day","cron_month","cron_week","cron_command","cron_user","crontab_name"];
	    var formData = new FormData();
	    if (cron_type=='upload'){
			var fileSelect = document.getElementById('cron_script');
			var files = fileSelect.files;		
			for (var i = 0; i < files.length; i++) {
				  var file = files[i];
				  formData.append('cron_script', file, file.name);
			}
	    }else if(cron_type=='online'){
	    	formData.append('cron_script', aceEditAdd.getSession().getValue());
	    }
		var form = document.getElementById('addCrontabForm');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;	
			idx = $.inArray(name, required);						
			if (idx >= 0 && value.length == 0){
	        	new PNotify({
	                title: 'Warning!',
	                text: '必填项不能为空',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
		    	btnObj.removeAttr('disabled');
		    	return false;
			};					
		};
		var ansible_server = new Array();
		$("select[name='deploy_server'] option:selected").each(function(){
			ansible_server.push($(this).val());
        });			
	    formData.append('cron_name',$('#cron_name').val());
	    formData.append('cron_minute',$('#cron_minute').val());
	    formData.append('cron_hour',$('#cron_hour').val());
	    formData.append('cron_month',$('#cron_month').val());
	    formData.append('cron_week',$('#cron_week').val());
	    formData.append('cron_day',$('#cron_day').val());
	    formData.append('server_model','custom');
	    formData.append('custom',ansible_server);
	    formData.append('cron_type',cron_type);
	    formData.append('cron_user',$('#cron_user').val());	
	    formData.append('cron_script_path',$('#cron_script_path').val());
	    formData.append('cron_log_path',$('#cron_log_path').val());
	    formData.append('cron_command',$('#cron_command').val());		
		$.ajax({
			url:'/sched/cron/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				if (response["code"] == "200"){
					btnObj.removeAttr('disabled');
	            	new PNotify({
	                    title: '<strong>操作成功:</strong>',
	                    text: "操作成功",
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
	         	    var trHtml = ''
		    		for (var i = 0; i < response["data"].length; i++) {
		    			if (response["data"][i]["result"]=='success'){
		    				trHtml += '<tr><td><strong>'+ response["data"][i]["assets"] +':</strong></td>'+ '<td><font color="green">'+ response["data"][i]["result"] +'</font></td></tr>'	  
		    			}else{
		    				trHtml += '<tr><td><strong>'+ response["data"][i]["assets"] +':</td>'+ '</strong><td><font color="red">'+ response["data"][i]["result"] +'</font></td></tr>'	  
		    			}  
	    			}
	         	    var vHtml = '<div class="row"><div class="col-lg-12"><table class="table table-bordered">'+ trHtml  + '</table></div></div>';	
	         	   $("#result").html(vHtml)
				}
				RefreshTable('#crontabList', '/api/sched/cron/');
				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	    	}
		})	    	
    });
    
	$('#crontabList tbody').on('click',"button[name='btn-script-edit']", function(){
		$('#add_deploy_tools').show();
		$('#add_deploy_result').show();	
		$('#add_crontab').hide();
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		$('#modf_crontab').val(vIds).show();
	    $.ajax({  
	        url : '/sched/cron/?id='+ vIds ,  
	        type : 'get', 
	        success : function(response){
	            	btnObj.removeAttr('disabled');
	            	if(response["code"] == "200"){
	            		DynamicSelect('deploy_server',response["data"]['cron_server_id']);
	            		$("#cron_name").val(response["data"]["cron_name"]).attr('disabled',true);
	            		$("#cron_minute").val(response["data"]["cron_minute"]);
	            		$("#cron_hour").val(response["data"]["cron_hour"]);
	            		$("#cron_day").val(response["data"]["cron_day"]);
	            		$("#cron_week").val(response["data"]["cron_week"]);
	            		$("#cron_month").val(response["data"]["cron_month"]);
	            		$("#cron_user").val(response["data"]["cron_user"]).attr('disabled',true);
	            		$("#cron_command").val(response["data"]["cron_command"]);
	            		$("#cron_script_path").val(response["data"]["cron_script_path"]);
	            		$("#cron_log_path").val(response["data"]["cron_log_path"]);
	            		$("#deploy_server").attr('disabled',true);
	            		$('.selectpicker').selectpicker('refresh');		 
	            		controlScriptHide(response["data"]["cron_type"]);
	            		$("button[name='btn-cron-scripts']").attr('disabled',true);
	            		$("#cron_script").attr('disabled',true);
	            		if (response["data"]["cron_type"]=='online'){
	            			aceEditAdd.setValue(response["data"]["cron_script"]);	            			
	            		}
	            		cron_type = response["data"]["cron_type"]
	            	}
	            	
	            },
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
		    	}	            
	    });		
	}); 
	
	$("#modf_crontab").on("click", function(){	  
    	  if($("#modf_crontab").val().length){
    			var btnObj = $(this);
    			btnObj.attr('disabled',true);    		  
    			var required = ["cron_minute","cron_hour","cron_day","cron_month","cron_week","cron_command","cron_user","crontab_name"];
//    		    var formData = {};
    			var data = {}
    		    if (cron_type=='upload'){
    		    	$("#cron_script").attr('disabled',true);
//    				var fileSelect = document.getElementById('cron_script');
//    				var files = fileSelect.files;		
//    				for (var i = 0; i < files.length; i++) {
//    					  var file = files[i];
//    					  formData.append('cron_script', file, file.name);
//    				}
    		    }else if(cron_type=='online'){
//    		    	formData.append('cron_script', aceEditAdd.getSession().getValue());
    		    	data['cron_script'] = aceEditAdd.getSession().getValue();
    		    }
    			var form = document.getElementById('addCrontabForm');
    			for (var i = 0; i < form.length; ++i) {
    				var name = form[i].name;
    				var value = form[i].value;	
    				idx = $.inArray(name, required);						
    				if (idx >= 0 && value.length == 0){
    		        	new PNotify({
    		                title: 'Warning!',
    		                text: '必填项不能为空',
    		                type: 'warning',
    		                styling: 'bootstrap3'
    		            }); 
    			    	btnObj.removeAttr('disabled');
    			    	return false;
    				};					
    			};
    			data['id'] = $("#modf_crontab").val()
				data['cron_name'] = $('#cron_name').val()
				data['cron_minute'] = $('#cron_minute').val()
				data['cron_hour'] = $('#cron_hour').val()
				data['cron_month'] = $('#cron_month').val()
				data['cron_week'] = $('#cron_week').val()
				data['cron_day'] = $('#cron_day').val()
				data['cron_type'] = cron_type
				data['cron_script_path'] = $('#cron_script_path').val()
				data['cron_log_path'] = $('#cron_log_path').val()
				data['cron_command'] = $('#cron_command').val() 			
    			$.ajax({
    				url:'/sched/cron/', //请求地址
    				type:"put",  //提交类似
    			    dataType: "json",
    				data:data,  //提交参数
    				success:function(response){
    					btnObj.removeAttr('disabled');
    					if (response["code"] == "200"){
    						btnObj.removeAttr('disabled');
    		            	new PNotify({
    		                    title: '<strong>操作成功:</strong>',
    		                    text: "操作成功",
    		                    type: 'success',
    		                    styling: 'bootstrap3'
    		                }); 
    		         	    var trHtml = ''
    			    		for (var i = 0; i < response["data"].length; i++) {
    			    			if (response["data"][i]["result"]=='success'){
    			    				trHtml += '<tr><td><strong>'+ response["data"][i]["assets"] +':</strong></td>'+ '<td><font color="green">'+ response["data"][i]["result"] +'</font></td></tr>'	  
    			    			}else{
    			    				trHtml += '<tr><td><strong>'+ response["data"][i]["assets"] +':</td>'+ '</strong><td><font color="red">'+ response["data"][i]["result"] +'</font></td></tr>'	  
    			    			}  
    		    			}
    		         	    var vHtml = '<div class="row"><div class="col-lg-12"><table class="table table-bordered">'+ trHtml  + '</table></div></div>';	
    		         	   $("#result").html(vHtml)
    					}
    					RefreshTable('#crontabList', '/api/sched/cron/');
    				},
    		    	error:function(response){
    		    		btnObj.removeAttr('disabled');
    		    	}
    			})
    	  }else{
				$.confirm({
				    title: '任务编辑',
				    content: '请先选择任务',
				    type: 'red',
				    typeAnimated: true,
				    buttons: {
				        close: function () {
				        }
				    }
				});	    		  
    	  }
  	}); 
	
	$('#crontabList tbody').on('click',"button[name='btn-script-view']", function(){
		$('#add_deploy_result').show();	
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
	    $.ajax({  
	        url : '/sched/cron/',  
	        type : 'POST', 
		    dataType: "json",
			data:{
				"id":vIds,
				"type":"view"
			},  //提交参数
	        success : function(response){
	            	btnObj.removeAttr('disabled');
	            	if(response["code"] == "200"){
		         	    var trHtml = ''
			    		for (var i = 0; i < response["data"].length; i++) {
			    			if (response["data"][i]["status"]=='success'){
			    				trHtml += '<tr><td><strong>'+ response["data"][i]["ip"] +':</strong></td>'+ '<td><font color="green">'+ response["data"][i]["msg"] +'</font></td></tr>'	  
			    			}else{
			    				trHtml += '<tr><td><strong>'+ response["data"][i]["ip"] +':</td>'+ '</strong><td><font color="red">'+ response["data"][i]["msg"] +'</font></td></tr>'	  
			    			}  
		    			}
		         	    var vHtml = '<div class="row"><div class="col-lg-12"><table class="table table-bordered">'+ trHtml  + '</table></div></div>';	
		         	   $("#result").html('<pre>'+ response["data"][0]["msg"] +'</pre>')
	            	}
	            	
	            },
		    	error:function(response){
		    		btnObj.removeAttr('disabled');
		    	}	            
	    });		
	}); 
	
	$('#crontabList tbody').on('click',"button[name='btn-script-delete']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
		var server = $(this).parent().parent().parent().find("td").eq(8).text(); 		
		$.confirm({
		    title: '删除确认',
		    content: server + ': ' +name,
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
		            url:"/sched/cron/",  
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
		        	btnObj.removeAttr('disabled');
		            return true;			            
		        },			        
		    }
		});		
	}); 
	
	$('#crontabList tbody').on('click',"button[name='btn-script-disabled']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
		var server = $(this).parent().parent().parent().find("td").eq(2).text(); 		
		$.confirm({
		    title: '禁用确认',
		    content: server + ': ' +name,
		    type: 'red',
		    buttons: {
		        禁用: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "post",  
				    dataType: "json",
					data:{
						"id":vIds,
						"type":"disabled"
					}, 		            
		            url:"/sched/cron/",  
		            error: function(request) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "禁用失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });       
		            },  
		            success: function(request) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "操作成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	RefreshTable('#crontabList', '/api/sched/cron/');
//		            	window.location.reload();
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
	
	$('#crontabList tbody').on('click',"button[name='btn-script-enable']", function(){
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
		var server = $(this).parent().parent().parent().find("td").eq(2).text(); 		
		$.confirm({
		    title: '启用确认',
		    content: server + ': ' +name,
		    type: 'red',
		    buttons: {
		        启用: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "post",  
				    dataType: "json",
					data:{
						"id":vIds,
						"type":"enable"
					}, 		            
		            url:"/sched/cron/",  
		            error: function(request) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "启动失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });       
		            },  
		            success: function(request) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "操作成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	RefreshTable('#crontabList', '/api/sched/cron/');
//		            	window.location.reload();
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