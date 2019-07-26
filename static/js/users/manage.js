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

function GetPermsOrGroups(url,uid){
	var aList = []
	var sList = []
	var url = url + '&id=' + uid
	response = requests('get',url)
	if(response["code"]=="200"){
		for (var i=0; i <response["data"].length; i++){
			if (response["data"][i]["apps_name"]){
				var name = response["data"][i]["apps_name"]+ ' - ' + response["data"][i]["name"]
			}else{
				var name = response["data"][i]["name"]
			}			
			if(response["data"][i]["status"]==1){
				sList.push({"id":response["data"][i]["id"],"name":name})
			}
			else{
				aList.push({"id":response["data"][i]["id"],"name":name})
			}
		}			
		
	}
	return {"group":sList,"all":aList}
}   

function GetUsersOfAssets(url,uid){
	var aList = []
	var sList = []
	var url = url + '&id=' + uid
	userAssetsList = requests('get',url)["data"]
	allAssetsList = requests('get','/api/assets/')
	if(allAssetsList.length){
		for (var i=0; i <allAssetsList.length; i++){
			var count = 0
			for (var j=0; j <userAssetsList.length; j++){
				if(userAssetsList[j]["id"]==allAssetsList[i]["id"]){
					count += 1
 				} 
			}
			var name = allAssetsList[i]["detail"]["ip"]+ ' | ' + allAssetsList[i]["project"]+' | '+allAssetsList[i]["service"]			
			if(count > 0 ){
				sList.push({"id":allAssetsList[i]["id"],"name":name})
			}
			else{
				aList.push({"id":allAssetsList[i]["id"],"name":name})
			}
		}				
	}
	return {"group":sList,"all":aList}
}

function GetUsersOfGroups(url,uid){
	var aList = []
	var uList = []
	var url = url + '&id=' + uid
	allUsers = requests('get','/user/manage/?type=get_users')
	groupUsers = requests('get',url)
	for (var i=0; i <allUsers["data"].length; i++){
		var count = 0
		for (var x=0; x <groupUsers["data"].length; x++){
			if (groupUsers["data"][x]["id"] == allUsers["data"][i]["id"]){
				count = count + 1
				break
			}
		}
		if (count > 0){
			uList.push({"id":allUsers["data"][i]["id"],"name":allUsers["data"][i]["username"]})
		}else{
			aList.push({"id":allUsers["data"][i]["id"],"name":allUsers["data"][i]["username"]})		
		}		
	}		
	return {"users":uList,"all":aList}
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

function InitDataTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	data,
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
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

function makeUserManageTableList(){
    var columns = [
                   {"data": "id"},
                   {"data": "username"},
                   {"data": "email"},
	               {"data": "is_superuser"},
	               {"data": "last_login"},
	               {"data": "date_joined"},
	               {"data": "is_active"},
	               ]
   var columnDefs = [
	    		        {
	   	    				targets: [3],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.is_superuser==true){
	   	    						return '<span class="label label-success">是</span>'
	   	    					}else{
	   	    						return '<span class="label label-danger">否</span>'
	   	    					}
	   	    				}
	    		        },  
	    		        {
	   	    				targets: [6],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.is_active==true){
	   	    						return '<span class="label label-success">已激活</span>'
	   	    					}else{
	   	    						return '<span class="label label-danger">未激活</span>'
	   	    					}
	   	    				}
	    		        }, 	    		        
	    		        {
   	    				targets: [7],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-user-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +  
	    	                           '<button type="button" name="btn-user-passwd" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-eye" aria-hidden="true"></span>' +	
	    	                           '</button>' + 		    	                           
	    	                           '<button type="button" name="btn-user-groups" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-groups"><span class="fa fa-users" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	
	    	                           '<button type="button" name="btn-user-perms" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-perms"><span class="fa fa-ban" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                           '<button type="button" name="btn-user-assets" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-assets"><span class="fa fa-desktop" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-user-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
	InitDataTable('userManageListTable','/api/user/',buttons,columns,columnDefs);	
}	

function makeGroupsManageTableList(){
    var columns = [
                   {"data": "id"},
                   {"data": "name"}
	               ]
   var columnDefs = [    		        
	    		        {
   	    				targets: [2],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-group-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                           '<button type="button" name="btn-group-users" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-group-users"><span class="fa fa-users" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-group-perms" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-group-perms"><span class="fa fa-ban" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-group-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
        	addGroups()
        }
    }]    
	InitDataTable('groupManageListTable','/api/group/',buttons,columns,columnDefs);	
}


function addGroups(){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加用户组',
        content: '<div class="form-group"><input type="text" name="group_name" placeholder="请输入名称" class="param_name form-control" /></div>',
        buttons: {
            '取消': function() {},
            '添加': {
                btnClass: 'btn-blue',
                action: function() {
                    var group_name = this.$content.find("[name='group_name']").val();
			    	$.ajax({  
			            type: "POST",  
			            url:"/api/group/",  
						data:{
							"name":group_name,
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
			            	new PNotify({
			                    title: 'Success!',
			                    text: '修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 				            		
			            	RefreshTable('#groupManageListTable', '/api/group/')
			            }  
			    	});
                }
            }
        }
    });	
}

$(document).ready(function() {	
	
	
	makeUserManageTableList()
	makeGroupsManageTableList()  
    
	$('#userManageListTable tbody').on('click',"button[name='btn-user-edit']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var username =  td.eq(1).text()
    	var email =  td.eq(2).text()
    	var superuser =  td.eq(3).text()
    	var is_active =  td.eq(7).text()
    	if(superuser=="否"){
    		var superUserSelect = '<select class="form-control" name="modf_superuser"><option selected="selected" name="modf_superuser" value="0">否</option><option name="modf_superuser" value="1">是</option></select>'
    	}else{
    		var superUserSelect = '<select class="form-control" name="modf_superuser"><option name="modf_superuser" value="0">否</option><option selected="selected" name="modf_superuser" value="1">是</option></select>'
    	}
    	if(is_active=="否"){
    		var isActiveSelect = '<select class="form-control" name="modf_is_active"><option selected="selected" name="modf_is_active" value="0">否</option><option name="modf_is_active" value="1">是</option></select>'
    	}else{
    		var isActiveSelect = '<select class="form-control" name="modf_is_active"><option name="modf_is_active" value="0">否</option><option selected="selected" name="modf_is_active" value="1">是</option></select>'
    	}    	
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ username +'</strong>资料',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">用户名<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text"  name="modf_username" value="'+ username +'" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">邮箱地址<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="modf_email" value="'+ email +'"  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">超级管理员<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              		superUserSelect +
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
	                    var username = this.$content.find("[name='modf_username']").val();
	                    var email = this.$content.find("[name='modf_email']").val();
	                    var superuser = this.$content.find("select[name='modf_superuser'] option:selected").val()
	                    var is_active = this.$content.find("select[name='modf_is_active'] option:selected").val()
				    	$.ajax({  
				            type: "POST",  
				            url:"/user/manage/",  
							data:{
								"type":"modf_user",
								"id":vIds,
				            	"username":username,
				            	"email":email,
				            	"is_superuser":superuser,
				            	"is_active":is_active,
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
					                    text: '修改成功',
					                    type: 'success',
					                    styling: 'bootstrap3'
					                }); 
					            	RefreshTable('#userManageListTable', '/api/user/')
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
	
	$('#userManageListTable tbody').on('click',"button[name='btn-user-passwd']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var username =  td.eq(1).text() 	
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ username +'</strong>密码',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">新密码<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="password"  name="modf_password" required="required" placeholder="新密码" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">确认密码<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="password" name="modf_c_password" required="required" placeholder="二次确认" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 		            
			          '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var password = this.$content.find("[name='modf_password']").val();
	                    var c_password = this.$content.find("[name='modf_c_password']").val();
				    	$.ajax({  
				            type: "POST",  
				            url:"/user/manage/",  
							data:{
								"type":"change_passwd",
								"id":vIds,
				            	"password":password,
				            	"c_password":c_password,
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

				            }  
				    	});
	                }
	            }
	        }
	    });
    });		
	
	
	$('#userManageListTable tbody').on('click',"button[name='btn-user-groups']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var username =  td.eq(1).text() 
    	$("#userGroupSubmit").val(vIds)
    	$("#myUserGroupsModalLabel").html('<h4 class="modal-title">修改<code>'+ username +'</code>用户分组</h4>')
    	$('select[name="user-group-doublebox"]').empty();
    	var data = GetPermsOrGroups('/user/manage/?type=get_user_group',vIds)
		$('select[name="user-group-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择用户组',
	        selectedListLabel: '已分配用户组',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });		
	
    $("#userGroupSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="user-group-doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/user/manage/",  
	            data:{
	            	"type":"modf_user_group",
					"id": vIds,
					"groups":vServer
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
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择任何用户组~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });		
	
 
    
    
	$('#userManageListTable tbody').on('click',"button[name='btn-user-perms']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var username =  td.eq(1).text() 
    	$("#userPermsSubmit").val(vIds)
    	$("#myUserPermsModalLabel").html('<h4 class="modal-title">修改<code>'+ username +'</code>用户权限</h4>')
    	$('select[name="user-perms-doublebox"]').empty();
    	var data = GetPermsOrGroups('/user/manage/?type=get_user_perms',vIds)
		$('select[name="user-perms-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择权限',
	        selectedListLabel: '已分配权限',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });	    
    
    $("#userPermsSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="user-perms-doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/user/manage/",  
	            data:{
	            	"type":"modf_user_perm",
					"id": vIds,
					"perms":vServer
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
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择任何权限~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });	    
	
	$('#userManageListTable tbody').on('click',"button[name='btn-user-assets']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var username =  td.eq(1).text() 
    	$("#userAssetsSubmit").val(vIds)
    	$("#myUserAssetsModalLabel").html('<h4 class="modal-title">修改<code>'+ username +'</code>用户资产</h4>')
    	$('select[name="user-assets-doublebox"]').empty();
    	var data = GetUsersOfAssets('/user/manage/?type=get_user_assets',vIds)
		$('select[name="user-assets-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择资产',
	        selectedListLabel: '已分配资产',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });	 
	
    $("#userAssetsSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="user-assets-doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/user/manage/",  
	            data:{
	            	"type":"modf_user_assets",
					"id": vIds,
					"assets":vServer
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
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择任何资产~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });		    
    
	$('#userManageListTable tbody').on('click',"button[name='btn-user-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>用户</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:"/api/user/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
//			            window.location.reload();
						RefreshTable('#userManageListTable', '/api/user/')
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

    $("#addUsersubmit").on('click', function() {
    	var form = document.getElementById('addUserForm');
    	var post_data = {};
    	for (var i = 1; i < form.length; ++i) {
    		var name = form[i].name;
    		var value = form[i].value;
    		if (value.length==0){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 
    			return false;
    		}else{
    			post_data[name] = value
    		}
    	};
    	post_data['type'] = "register"
    	$.ajax({  
            type: "POST",             
            url:"/user/manage/",  
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
	            	RefreshTable('#userManageListTable', '/api/user/')
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
		
	$('#groupManageListTable tbody').on('click',"button[name='btn-group-edit']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var group_name =  td.eq(1).text()  	
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ group_name +'</strong>资料',
	        content: '<div class="form-group"><input type="text" value="'+ group_name +'" name="group_name" placeholder="请输入名称" class="form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var group_name = this.$content.find("[name='group_name']").val();
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/group/" + vIds +"/",  
							data:{
								"name":group_name,
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
					            	new PNotify({
					                    title: 'Success!',
					                    text: '修改成功',
					                    type: 'success',
					                    styling: 'bootstrap3'
					                }); 
					            	RefreshTable('#groupManageListTable', '/api/group/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#groupManageListTable tbody').on('click',"button[name='btn-group-perms']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var groupname =  td.eq(1).text() 
    	$("#groupPermsSubmit").val(vIds)
    	$("#myGroupsPermsModalLabel").html('<h4 class="modal-title">修改<code>'+ groupname +'</code>用户组权限</h4>')
    	$('select[name="group-perms-doublebox"]').empty();
    	var data = GetPermsOrGroups('/group/manage/?type=get_group_perms',vIds)
		$('select[name="group-perms-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择权限',
	        selectedListLabel: '已分配权限',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });		
	
    $("#groupPermsSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="group-perms-doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/group/manage/",  
	            data:{
	            	"type":"modf_group_perm",
					"id": vIds,
					"perms":vServer
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
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择任何用户组~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
    });
    
	$('#groupManageListTable tbody').on('click',"button[name='btn-group-users']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var groupname =  td.eq(1).text() 
    	$("#groupUsersSubmit").val(vIds)
    	$("#myGroupUsersModalLabel").html('<h4 class="modal-title">修改<code>'+ groupname +'</code>用户组成员</h4>')
    	$('select[name="group-users-doublebox"]').empty();
    	var data = GetUsersOfGroups('/group/manage/?type=get_group_users',vIds)
		$('select[name="group-users-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择成员',
	        selectedListLabel: '已选择成员',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["users"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });	
    
    $("#groupUsersSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var users = $('[name="group-users-doublebox"]').val()
    	if (users){
	    	$.ajax({  
	            type: "POST",             
	            url:"/group/manage/",  
	            data:{
	            	"type":"modf_group_users",
					"id": vIds,
					"users":users
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
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择任何用户组~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });	    
    
	$('#groupManageListTable tbody').on('click',"button[name='btn-group-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>用户</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/group/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
						RefreshTable('#groupManageListTable', '/api/group/')
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