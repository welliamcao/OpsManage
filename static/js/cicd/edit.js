function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);
}

function AssetsTypeSelect(model,ids){ 
	$.ajax({
		dataType: "JSON",
		url:'/assets/server/query/', //请求地址
		type:"POST",  //提交类似
		async:false,
		data:{
			"query":model,
			"id":ids
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
function get_url_param(name) {
	 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	 var r = window.location.search.substr(1).match(reg);
	 if (r != null) return unescape(r[2]); return null; 
}

$(document).ready(function() {
	
	 $("#project_env").change(function(){
		   var obj = document.getElementById("project_env"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   if (value=="uat"){
			   $("#extConfig").show();  	   
		   }
		   else {
			   $("#extConfig").hide();  
		   }		 
	 });	
	
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
	url = '/apps/config/?type=info&id=' + get_url_param('id')
	var project = requests('get',url)
	if (project["code"]!=200){
		 window.location.href="/404/";
	}else{
		AssetsTypeSelect("service",project["data"]["project_service"]) 
		$("#deploy_project").val(project["data"]["project_id"]);
		$("#deploy_service").val(project["data"]["service_name"]);
		$("#project_name").val(project["data"]["project_name"]);
		DynamicSelect('project_env',project["data"]["project_env"])
		DynamicSelect('project_repertory',project["data"]["project_repertory"])
		DynamicSelect('project_is_include',project["data"]["project_is_include"])
		$("#project_address").val(project["data"]["project_address"]);
		$("#project_model").val(project["data"]["project_model"]);
		$("#project_dir").val($("#project_dir").val()+project["data"]["project_name"]+'/')
		$("#project_repo_dir").val(project["data"]["project_repo_dir"])
		$("#project_exclude").val(project["data"]["project_exclude"]);
		$("#project_user").val(project["data"]["project_user"]);
		try
			{
			$("#project_target_root").val(project["data"]["project_target_root"]);		  
			}
		catch(err)
			{
			$("#project_target_root").val("");		
			}
		try
			{
			$("#project_logpath").val(project["data"]["project_logpath"]);		  
			}
		catch(err)
			{
			$("#project_logpath").val("");		
			}	
		$("#project_remote_command").val(project["data"]["project_remote_command"]);
		$("#project_pre_remote_command").val(project["data"]["project_pre_remote_command"]);
		//选中主机
		for (var i = 0; i < project["data"]["project_servers"].length; ++i) {
			$("#server option[value='" + project["data"]["project_servers"][i] +"']").attr("selected",true);
		}
		$('.selectpicker').selectpicker('refresh');			
		
		var compile_type = project["data"]["project_type"];
		if ($("#project_local_command").length){
			var aceEditAdd = setAceEditMode("project_local_command","ace/mode/sh","ace/theme/terminal");
			if (compile_type=='compile'){
				$("#compile").show()
				aceEditAdd.setValue(project["data"]["project_local_command"]);
			}
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
	}
	
    $('#btn_modf_project').click(function(){ 
		var btnObj = $(this);
		btnObj.attr('disabled',true);
    	var required = ["project_name","project_env","project_repertory","project_address","server","project_user","dir"];
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
    		formData.append('type','update');	
    		formData.append('id',get_url_param('id'));	
    	    formData.append('project_env',$('#project_env').val());	
    	    formData.append('project_name',$('#project_name').val());	 
    	    formData.append('project_address',$('#project_address').val());	
    	    formData.append('project_user',$('#project_user').val());
    	    formData.append('project_target_root',$('#project_target_root').val());	
    	    formData.append('project_pre_remote_command',$('#project_pre_remote_command').val());
    	    formData.append('project_remote_command',$('#project_remote_command').val());
    	    formData.append('project_exclude',$('#project_exclude').val());	
    	    formData.append('project_dir',$('#project_dir').val());	
    	    formData.append('project_logpath',$('#project_logpath').val());
    	    formData.append('project_is_include',$('#project_is_include  option:selected').val());	
    	    formData.append('project_repo_dir',$('#project_repo_dir').val());
    	    formData.append('project_repo_user',$('#project_repo_user').val());	
    	    formData.append('project_repo_passwd',$('#project_repo_passwd').val());
    	    formData.append('project_audit_group',$('#project_audit_group  option:selected').val());	
    	    formData.append('project_repertory',$('#project_repertory option:selected').val());
    	    formData.append('project_model',$('#project_model option:selected').val());	
    	    formData.append('project_servers',serverList);	
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
		                    text: "修改成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
    				}
    				else {
    		           	new PNotify({
 		                   title: 'Ops Failed!',
 		                   text: response.responseText,
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
	
})