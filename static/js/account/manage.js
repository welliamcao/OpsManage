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

function GetPermsOrRoles(url,uid){
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
			var name = allAssetsList[i]["detail"]["ip"]		
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

function GetUsersOfRoles(url,uid){
	var aList = []
	var uList = []
	var url = url + '&id=' + uid
	allUsers = requests('get','/account/user/manage/?type=get_users')
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

function InitUrlDataTable(tableId,url,buttons,columns,columnDefs){
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

function InitDataTable(tableId,dataList,buttons,columns,columnDefs,select){
	var dataTableStayle = {
		    "dom": "Bfrtip",
		    "buttons":buttons,
    		"bScrollCollapse": false, 				
    	    "bRetrieve": true,			
    		"destroy": true, 
    		"data":	dataList,
    		"pageLength": 50,
    		"columns": columns,
    		"columnDefs" :columnDefs,
    		"language" : language,
    		"autoWidth": false	    			
		}	
	switch(select) {
	    case "multi":
	    	dataTableStayle["select"] = {
            	"style": 'multi',
                "selector": 'td:first-child'	    			
    		}
	       break;
	    case "os":
	    	dataTableStayle["select"] =	{
            	"style": 'os',
                "selector": 'td:first-child'	    			
    		}
	       break;
	} 	
	oOverviewTable =$('#'+tableId).dataTable(dataTableStayle);
}

function AutoReload(tableId,url){
	  RefreshTable('#'+tableId, url);
	  setTimeout(function(){AutoReload(url);}, 30000);
}

function makeUserManageTableList(){
    var columns = [
                   {"data": "id"},
                   {"data": "username"},
                   {"data": "name"},
                   {"data": "mobile"},
                   {"data": "email"},
	               {"data": "is_superuser"},
	               {"data": "post"},
	               {"data": "superior_name"},
	               {"data": "last_login"},
	               {"data": "date_joined"},
	               {"data": "is_active"},
	               ]
   var columnDefs = [
	    		        {
	   	    				targets: [5],
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
	   	    					if(row.post=="manage"){
	   	    						return '<code>管理人员</code>'
	   	    					}else{
	   	    						return '<code>普通员工</code>'
	   	    					}
	   	    				}
	    		        }, 	    		        
	    		        {
	   	    				targets: [10],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.is_active==true){
	   	    						return '<span class="label label-success">已激活</span>'
	   	    					}else{
	   	    						return '<span class="label label-danger">未激活</span>'
	   	    					}
	   	    				}
	    		        }, 	    		        
	    		        {
   	    				targets: [11],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-user-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +  
	    	                           '<button type="button" name="btn-user-passwd" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-eye" aria-hidden="true"></span>' +	
	    	                           '</button>' + 		    	                           
	    	                           '<button type="button" name="btn-user-roles" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-Roles"><span class="fa fa-users" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	
	    	                           '<button type="button" name="btn-user-perms" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-perms"><span class="fa fa-ban" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                           '<button type="button" name="btn-user-assets" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-user-assets"><span class="fa fa-desktop" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-user-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
        	let dataList = requests("get","/api/account/user/?post=manage")
        	makeSelectpicker("superior","name",dataList)        	
        	$('#myAddUserModal').modal("show")
        }
    }]    
	InitUrlDataTable('userManageListTable','/api/account/user/',buttons,columns,columnDefs);	
}	

function makeRolesManageTableList(){
    var columns = [
                   {"data": "id"},
                   {"data": "name"},
                   {"data": "desc"}
	               ]
   var columnDefs = [    		        
	    		        {
   	    				targets: [3],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-role-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' + 
	    	                           '<button type="button" name="btn-role-users" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-role-users"><span class="fa fa-users" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-role-perms" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-role-perms"><span class="fa fa-ban" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-role-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
        	addRoles()
        }
    }]    
	InitUrlDataTable('roleManageListTable','/api/account/role/',buttons,columns,columnDefs);	
}


function addRoles(){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加用户角色',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			        '<div class="form-group">' +
				        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">角色名称: <span class="required">*</span>' +
				        '</label>' +
				        '<div class="col-md-6 col-sm-6 col-xs-12">' +
				          '<input type="text"  name="name" value="" required="required" class="form-control col-md-7 col-xs-12">' +
				        '</div>' +
			        '</div>' +	
			        '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注信息: <span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			          '<input type="text"  name="desc" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
		        '</div>' +			        
			    '</form>',
        buttons: {
            '取消': function() {},
            '添加': {
                btnClass: 'btn-blue',
                action: function() {
                	var formData = {};	
            		var vipForm = this.$content.find('input');                	
            		for (var i = 0; i < vipForm.length; ++i) {
            			var name =  vipForm[i].name
            			var value = vipForm[i].value 
            			if (name.length >0 && value.length > 0){
            				formData[name] = value	
            			};		            						
            		};	
			    	$.ajax({  
			            type: "POST",  
			            url:"/api/account/role/",  
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
			            	new PNotify({
			                    title: 'Success!',
			                    text: '修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 				            		
			            	RefreshTable('#roleManageListTable', '/api/account/role/')
			            }  
			    	});
                }
            }
        }
    });	
}


function makeStructureTreeTables(){
//	RefreshEnvInfo()
    var columns = [
                    {
                    	"data": "id",
                    	"defaultContent" :"",
                    },
                    {
                    	"data": "text",
                    	"defaultContent" :"",
                    },
					{
                    	"data": "desc",
                    	"defaultContent" :"",
					},
					{
						"data": "manage_name",
						"defaultContent" :"",
					},						
                    {
						"data": "type",
                    	"defaultContent" :"",
                    },
					{
                    	"data": "mail_group",
                    	"defaultContent" :"",
                    },
					{
                    	"data": "wechat_webhook_url",
                    	"defaultContent" :"",
                    },
					{
                    	"data": "dingding_webhook_url",
                    	"defaultContent" :"",
                    }
	               ]
    var columnDefs = [		
				        {
							targets: [4],
							render: function(data, type, row, meta) {		    	    					
				                if(row.type=="unit"){
				                	return "单位"
				                }else{
				                	return "部门"
				                }
							},
							"className": "text-center",
				        },    	
	    		        {
    	    				targets: [8],
    	    				render: function(data, type, row, meta) {		    	    					
    	                        return '<div class="btn-group  btn-group-xs">' +
    	                        	   	'<button type="button" name="btn-structure-root-tree" value="'+ row.tree_id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
    	                           		'</button>' + 	    	                        
    	                           		'<button type="button" name="btn-structure-root-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
    	                           		'</button>' + 	    	                           
    	                           		'<button type="button" name="btn-structure-root-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
        	let dataList = requests("get","/api/account/user/")
        	makeSelectpicker("structure-node-manage","username",dataList) 	
        	$('#addStructureRootModal').modal("show");	
        }
    }]
	InitUrlDataTable('structureRootTableLists',"/api/account/structure/nodes/",buttons,columns,columnDefs)			
}  	


function resfreshJSTree(ids,dataList){ 
	$(ids).jstree(true).settings.core.data = dataList;
	$(ids).jstree(true).refresh();
}
function drawTree(ids,dataList){ 
	$(ids).jstree('destroy');
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if (op === "move_node" || op === "copy_node") {	    	    	
	    	        return false;
	    	    }
	    	    return true;
	    	},
	      'data' : dataList
	    },	    
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],
	    'state': {
	             "opened":true,
	     },	    
	    "contextmenu":{
		    	select_node:true,
		    	show_at_node:false,
		    	'items': customMenu
		      }	    
	});	
}

function create_nodes(obj,inst){
	var userList = requests("get","/api/account/user/")
	var userHtml = '<select required="required" class="form-control" name="manage"  autocomplete="off">'
	var userSelectHtml = '<option value="">无</option>';
	for (var i=0; i <userList.length; i++){
		userSelectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 						 
	};  
	userHtml =  userHtml + userSelectHtml + '</select>';	
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加部门',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			               '<input type="text"  name="text" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +				          
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="desc" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			            		userHtml +
			            '</div>' +
			          '</div>' +				          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">邮件 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="mail_group" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +			          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">微信 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="wechat_webhook_url" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' + 
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">钉钉 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			               '<input type="text"  name="dingding_webhook_url" value="" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +			          
			        '</form>',
        buttons: {
            '取消': function() {},
            '添加': {
                btnClass: 'btn-blue',
                action: function() {
                	var formData = {};	
            		var vipForm = this.$content.find('input,select');                	
            		for (var i = 0; i < vipForm.length; ++i) {
            			var name =  vipForm[i].name
            			var value = vipForm[i].value 
            			if (name.length >0 && value.length > 0){
            				formData[name] = value	
            			};		            						
            		};	 		
					formData["parent"] = obj.original["id"]
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:'/api/account/structure/nodes/',  
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
			                    text: '业务添加成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	inst.create_node(obj, data, "last")
			            }  
			    	});
                }
            }
        }
    })         	
}

function modf_nodes(obj,inst){
	var userList = requests("get","/api/account/user/")
	var userHtml = '<select required="required" class="form-control" name="manage"  autocomplete="off">'
	var userSelectHtml = '<option value="">无</option>';
	for (var i=0; i <userList.length; i++){
		if (obj.original["manage"]==userList[i]["id"]){
			userSelectHtml += '<option selected="selected" value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>'
		}else{
			userSelectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>'
		}
		 						 
	};  
	userHtml =  userHtml + userSelectHtml + '</select>';
	console.log(obj.original)
    $.confirm({
        icon: 'fa fa-plus',
        type: 'blue',
        title: '修改部门',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			        '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称<span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			           '<input type="text"  name="text" value="'+  obj.original["text"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
			      '</div>' +				          
			      '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注 <span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			          '<input type="text"  name="desc" value="'+ obj.original["desc"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
			      '</div>' +
			      '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人 <span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			        		userHtml +
			        '</div>' +
			      '</div>' +			      
			      '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">邮件 <span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			          '<input type="text"  name="mail_group" value="'+ obj.original["mail_group"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
			      '</div>' +			          
			      '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">微信<span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			          '<input type="text"  name="wechat_webhook_url" value="'+ obj.original["wechat_webhook_url"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
			      '</div>' + 
			      '<div class="form-group">' +
			        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">钉钉 <span class="required">*</span>' +
			        '</label>' +
			        '<div class="col-md-6 col-sm-6 col-xs-12">' +
			           '<input type="text"  name="dingding_webhook_url" value="'+ obj.original["dingding_webhook_url"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
			        '</div>' +
			      '</div>' +			          
			    '</form>',
        buttons: {
            '取消': function() {},
            '修改': {
                btnClass: 'btn-blue',
                action: function() {
                	var formData = {};	
            		var vipForm = this.$content.find('input,select');                	
            		for (var i = 0; i < vipForm.length; ++i) {
            			var name =  vipForm[i].name
            			var value = vipForm[i].value 
            			if (name.length >0 && value.length > 0){
            				formData[name] = value	
            			};		            						
            		};	 		
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:'/api/account/structure/nodes/'+obj.original["id"]+'/',  
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
			                    text: '业务修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	inst.rename_node(obj,data["text"])
//			            	resfreshJSTree('#businessTree',requests('get','/api/business/tree/'))
//			            	RefreshTable('structureRootTableLists', '/api/account/structure/nodes/')
			            }  
			    	});
                }
            }
        }
    })         	
}

function delete_nodes(obj,inst){
  	$.confirm({
  	    title: '删除确认?',
  	    type: 'red',
  	    content: "<strong>业务线：</strong>"+ obj.original["text"] +"<br><strong>路径：</strong>【"+ obj.original["paths"] +"】<br><strong>提醒：</strong>删除时会一并删除下面的子业务线。",
  	    buttons: {
  	        确认: function () {
  			$.ajax({
  				  type: 'DELETE',
  				  url:'/api/account/structure/nodes/' + obj.original["id"] + '/',
  			      success:function(response){	
		            	new PNotify({
		                    title: 'Success!',
		                    text: '业务删除成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	inst.delete_node(obj)
		            	RefreshTable('structureRootTableLists', '/api/account/structure/nodes/');		            
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
}

function customMenu(node) {
    var items = {
            "new":{  
                "label":"添加部门",  
                "icon": "glyphicon glyphicon-plus",
                "action":function(data){
                	var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
                	create_nodes(obj,inst)
                }  
            },
            "modf":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "修改资料",
					"shortcut_label"	: 'F2',
					"icon"				: "glyphicon glyphicon-edit",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						modf_nodes(obj,inst)						
					}
            },
            "del":{
        		"separator_before"	: false,
				"separator_after"	: false,
				"_disabled"			: false, 
				"label"				: "删除部门",
				"shortcut_label"	: 'F2',
				"icon"				: "fa fa fa-remove",
				"action"			: function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);		
					delete_nodes(obj,inst)
				}
            },            
        }  
    return items
}

function makeStructureChildrenNodesTables(treeDataList){
    var columns = [
			        {
			        	"data": "id",
			        	"defaultContent" :"",
			        },
			        {
			        	"data": "text",
			        	"defaultContent" :"",
			        },
					{
			        	"data": "desc",
			        	"defaultContent" :"",
					},						
			        {
						"data": "type",
			        	"defaultContent" :"",
			        },
					{
			        	"data": "mail_group",
			        	"defaultContent" :"",
			        },
					{
			        	"data": "wechat_webhook_url",
			        	"defaultContent" :"",
			        },
					{
			        	"data": "dingding_webhook_url",
			        	"defaultContent" :"",
			        }
	               ]
    var columnDefs = [	                      
				        {
							targets: [3],
							render: function(data, type, row, meta) {		    	    					
				                if(row.type=="unit"){
				                	return "单位"
				                }else{
				                	return "部门"
				                }
							},
							"className": "text-center",
				        }                    
    		      ]	
 var buttons = []
    InitDataTable('structureChildrenNodesTableLists',treeDataList,buttons,columns,columnDefs)			
} 

function makeMemberTableList(dataList,select_node){
    var columns = [		  
		        	{
		               "orderable": false,
		               "data":      null,
		               "className": 'select-checkbox', 
		               "defaultContent": ''
		           },      	
                   {"data": "username"},		                       
                   {"data": "name"},     
                   {
                	   "data": "email",
                	   "defaultContent": ''
                   },
	               {
	            	   "data": "post",
	            	   "defaultContent": ''
	               },
	               {
	            	   "data": "superior_name",
	            	   "defaultContent": ''
	               },	               
	               {
	            	   "data": "mobile",
	            	   "defaultContent": ''
	               }
	               ]
   var columnDefs = [                      	    		     		    		    	    		    
				       {
							targets: [4],
							render: function(data, type, row, meta) {		    	    					
				               if(row.post=="manage"){
				               	return "管理人员"
				               }else{
				               	return "普通员工"
				               }
							},
							"className": "text-center",
				       },  	    		        
	    		      ]	
    var buttons = [
        {
           text: '关联',
           className: "btn-sm",
           action: function (e, dt, button, config) {        	
        	let dataList = requests("get","/api/account/structure/nodes/member/"+ select_node["id"] +"/?type=unallocated")
        	if (dataList.length){
        		makeSelectpicker("addStructureMemberSelect","username",dataList)
        		$('#addStructureMemberModal').modal("show");
        		$("#addStructureMemberModalLabel").html('<h4 class="modal-title" id="addStructureMemberModalLabel"><code>'+ select_node["paths"] +'</code> 关联成员</h4>')
        		$("#addStructureMemberSubmit").val(select_node["id"])         		
        	}else{
        		$.alert({
        		    title: '操作失败',
        		    content: '没有的用户可以进行关联！',
        		    type: 'red',		    
        		});	            		
        	}            	
           }
        },     
        {
            text: '取消',
            className: "btn-sm",
            action: function (e, dt, button, config) {        	
            	let dataList = dt.rows('.selected').data()
            	var vIdsList = new Array();
            	if (dataList.length==0){
            		$.alert({
            		    title: '操作失败',
            		    content: '批量更新资产失败，请先选择资产',
            		    type: 'red',		    
            		});	            		
            	}else{ 
            		abolishUserBind(select_node,dataList)
            	}                 	
            }
        },                             
        {
            text: '全选',
            className: "btn-sm",
            action: function (e, dt, button, config) {
            	dt.rows().select();
            }
        },        
        {
            text: '反选',
            className: "btn-sm",
            action: function (e, dt, button, config) {
            	dt.rows().deselect();
            }
        }    	
    ]    
	InitDataTable('structureLastNodesMemberTableLists',dataList,buttons,columns,columnDefs,'multi');	
}

function makeSelectpicker(ids, key, dataList){
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i][key] +'</option>' 					 
	};                        
	selectHtml =  selectHtml + '</select>';
	document.getElementById(ids).innerHTML = selectHtml;
	$("#"+ids).selectpicker('refresh');
}	

function abolishUserBind(select_node,dataList){
  	$.confirm({
  	    title: '确认取消用户关联?',
  	    type: 'red',
  	    content: "将选定用户，从【"+ select_node["paths"] +"】用户组移除？",
  	    buttons: {
  	        确认: function () {
				let formData = new FormData();
				for (var i = 0; i < dataList.length; ++i) {
					formData.append('user', dataList[i]["id"]);
				};	            	            
				$.ajax({  
					cache: true,  
					type: "DELETE",  
					url:'/api/account/structure/nodes/member/'+ select_node["id"] + '/',  
					data:formData,
					processData: false,
					contentType: false,	
					async: false,  
					error: function(request) {  
						new PNotify({
							title: 'Ops Failed!',
							text: request.responseText,
							type: 'error',
							styling: 'bootstrap3'
						});       
					},  
					success: function(data) {  
						RefreshTable("#structureLastNodesMemberTableLists", '/api/account/structure/nodes/member/'+ select_node["id"] + '/')		
					}  
				});		        
  	        },
  	       	 取消: function () {
  	            return true;
  	        },
  	    }
  	}); 	
}

$(document).ready(function() {	
	
	
	makeUserManageTableList()
	
	makeRolesManageTableList()  
	
	
	
	$('#userManageListTable tbody').on('click',"button[name='btn-user-edit']",function(){
    	let vIds = $(this).val();
    	let td = $(this).parent().parent().parent().find("td")
    	let username =  td.eq(1).text()
    	let name =  td.eq(2).text()
    	let mobile =  td.eq(3).text()
    	let email =  td.eq(4).text()
    	let superuser =  td.eq(5).text()
    	let post =  td.eq(6).text()  
    	let superior = td.eq(7).text()
    	let is_active =  td.eq(9).text()
    	
    	
		let selectHtmls = '<select class="form-control"  name="superior" title="上级"><option value="">无</option>'
    	let optionHtml = ''
    	let dataList = requests("get","/api/account/user/?post=manage")
		for (var i=0; i <dataList.length; i++){
			console.log(superuser)
			if (superuser==dataList[i]['name']){
				optionHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+ dataList[i]['name'] +'</option>' 	
			}else{
				optionHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]['name'] +'</option>' 	
			}
							 
		}; 
		
		selectHtmls = selectHtmls + optionHtml + '</select>';    	
    	
    	if(superuser=="否"){
    		var superUserSelect = '<select class="form-control" name="is_superuser"><option selected="selected"  value="0">否</option><option value="1">是</option></select>'
    	}else{
    		var superUserSelect = '<select class="form-control" name="is_superuser"><option  value="0">否</option><option selected="selected" value="1">是</option></select>'
    	}
    	if(is_active=="否"){
    		var isActiveSelect = '<select class="form-control" name="is_active"><option selected="selected"  value="0">否</option><option value="1">是</option></select>'
    	}else{
    		var isActiveSelect = '<select class="form-control" name="is_active"><option  value="0">否</option><option selected="selected" value="1">是</option></select>'
    	} 
    	if(post=="管理人员"){
    		var postSelect = '<select class="form-control" name="post"><option selected="selected"  value="manage">管理人员</option><option value="staff">普通员工</option></select>'
    	}else{
    		var postSelect = '<select class="form-control" name="post"><option selected="selected"  value="staff">普通员工</option><option value="manage">管理人员</option></select>'
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
			                '<input type="text"  name="username" value="'+ username +'" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">中文名<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text"  name="name" value="'+ name +'" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +	
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">电话号码<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text"  name="mobile" value="'+ mobile +'" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +			            
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">邮箱地址<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="email" value="'+ email +'"  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">职务<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              		postSelect +
			              '</div>' +
			            '</div>' +				            
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">上级<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              		selectHtmls +
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
	                	var formData = {};	
	            		var vipForm = this.$content.find('input,select');                	
	            		for (var i = 0; i < vipForm.length; ++i) {
	            			var name =  vipForm[i].name
	            			var value = vipForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/account/user/"+vIds+"/",  
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
				            	RefreshTable('#userManageListTable', '/api/account/user/')
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
				            url:"/account/user/manage/",  
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
	
	
	$('#userManageListTable tbody').on('click',"button[name='btn-user-roles']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var username =  td.eq(1).text() 
    	$("#userRolesubmit").val(vIds)
    	$("#myUserRolesModalLabel").html('<h4 class="modal-title">修改<code>'+ username +'</code>用户角色</h4>')
    	$('select[name="user-group-doublebox"]').empty();
    	var data = GetPermsOrRoles('/account/user/manage/?type=get_user_role',vIds)
		$('select[name="user-group-doublebox"]').doublebox({
	        nonSelectedListLabel: '选择用户角色',
	        selectedListLabel: '已分配用户角色',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });		
	
    $("#userRolesubmit").on('click', function() {
    	var vIds = $(this).val();
    	var roles = $('[name="user-group-doublebox"]').val()
    	if (roles){
	    	$.ajax({  
	            type: "POST",             
	            url:"/account/user/manage/",  
	            data:{
	            	"type":"modf_user_role",
					"id": vIds,
					"roles":roles
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
	    	    content: "没有选择任何用户角色~",
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
    	var data = GetPermsOrRoles('/account/user/manage/?type=get_user_perms',vIds)
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
	            url:"/account/user/manage/",  
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
    	var data = GetUsersOfAssets('/account/user/manage/?type=get_user_assets',vIds)
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
	            url:"/account/user/manage/",  
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
					url:"/api/account/user/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
//			            window.location.reload();
						RefreshTable('#userManageListTable', '/api/account/user/')
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
    	$.ajax({  
            type: "POST",             
            url:"/api/account/user/",  
            data:$("#addUserForm").serialize(),
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });       
            },  
            success: function(response) {  
	            RefreshTable('#userManageListTable', '/api/account/user/') 				            		
            }
    	}); 	
    });		
		
	$('#roleManageListTable tbody').on('click',"button[name='btn-role-edit']",function(){
    	let vIds = $(this).val();
    	let td = $(this).parent().parent().parent().find("td")
    	let role_name =  td.eq(1).text()  	
    	let role_desc =  td.eq(2).text() 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<strong>'+ role_name +'</strong>资料',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
					     '<div class="form-group">' +
						        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">角色名称: <span class="required">*</span>' +
						        '</label>' +
						        '<div class="col-md-6 col-sm-6 col-xs-12">' +
						          '<input type="text"  name="name" value="'+ role_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
						        '</div>' +
					        '</div>' +	
					     '<div class="form-group">' +
					        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注信息: <span class="required">*</span>' +
					        '</label>' +
					        '<div class="col-md-6 col-sm-6 col-xs-12">' +
					          '<input type="text"  name="desc" value="'+ role_desc +'" required="required" class="form-control col-md-7 col-xs-12">' +
					        '</div>' +
					     '</div>' +			        
				    '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	            		var vipForm = this.$content.find('input');                	
	            		for (var i = 0; i < vipForm.length; ++i) {
	            			var name =  vipForm[i].name
	            			var value = vipForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/account/role/" + vIds +"/",  
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
					            	new PNotify({
					                    title: 'Success!',
					                    text: '修改成功',
					                    type: 'success',
					                    styling: 'bootstrap3'
					                }); 
					            	RefreshTable('#roleManageListTable', '/api/account/role/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#roleManageListTable tbody').on('click',"button[name='btn-role-perms']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var groupname =  td.eq(1).text() 
    	$("#groupPermsSubmit").val(vIds)
    	$("#myRolesPermsModalLabel").html('<h4 class="modal-title">修改<code>'+ groupname +'</code>用户角色权限</h4>')
    	$('select[name="group-perms-doublebox"]').empty();
    	var data = GetPermsOrRoles('/account/role/manage/?type=get_role_perms',vIds)
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
	            url:"/account/role/manage/",  
	            data:{
	            	"type":"modf_role_perm",
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
	    	    content: "没有选择任何用户角色~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
    });
    
	$('#roleManageListTable tbody').on('click',"button[name='btn-role-users']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var groupname =  td.eq(1).text() 
    	$("#roleUsersSubmit").val(vIds)
    	$("#myRoleUsersModalLabel").html('<h4 class="modal-title">修改<code>'+ groupname +'</code>用户角色成员</h4>')
    	$('select[name="role-users-doublebox"]').empty();
    	var data = GetUsersOfRoles('/account/role/manage/?type=get_role_users',vIds)
		$('select[name="role-users-doublebox"]').doublebox({
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
    
    $("#roleUsersSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var users = $('[name="role-users-doublebox"]').val()
    	if (users){
	    	$.ajax({  
	            type: "POST",             
	            url:"/account/role/manage/",  
	            data:{
	            	"type":"modf_role_users",
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
	    	    content: "没有选择任何用户角色~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });	    
    
	$('#roleManageListTable tbody').on('click',"button[name='btn-role-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>用户</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/account/role/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
						RefreshTable('#roleManageListTable', '/api/account/role/')
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

	makeStructureTreeTables()	
	
    $('#addStructureRootSubmit').on('click', function() {   	 	
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/account/structure/nodes/",  
            data:$('#structureRootForm').serialize(),
            async: false,  
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
                    text: '节点添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('#structureRootTableLists', '/api/account/structure/nodes/');
            	$('#addBusinessRootModal').modal("hide");
            }  
    	});  	
    });		
	
	let dataList = requests("get","/api/account/structure/")
	
	drawTree('#structureTree',dataList)
	
	$("#structureTree").click(function () {
	     var position = 'last';
	     let select_node = $(this).jstree("get_selected",true)[0]["original"];
	     
	     if (select_node["last_node"] == 0 && select_node["parentId"] > 0){
				$.ajax({
					  type: 'GET',
					  url: '/api/account/structure/nodes/'+ select_node["id"] +'/?type=children',
				      success:function(response){	
				    	  $("#childrenNodes").show()
				    	  $("#nodesAssets").hide()
				    	  $("#nodeName").html('<h2 id="nodeName">'+ select_node["paths"] +'_子部门 <small>Sub Department</small></h2>')
				    	  if ($('#structureChildrenNodesTableLists').hasClass('dataTable')) {
				            dttable = $('#structureChildrenNodesTableLists').dataTable();
				            dttable.fnClearTable(); //清空table
				            dttable.fnDestroy(); //还原初始化datatable
				    	  }			    	  
				    	  makeStructureChildrenNodesTables(response)
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
	     }else if(select_node["last_node"] == 1){
				$.ajax({
					  type: 'GET',
					  url: '/api/account/structure/nodes/member/'+ select_node["id"] + '/',
				      success:function(response){	
				    	  $("#childrenNodes").hide()
				    	  $("#nodesAssets").show()
				    	  $("#lastNodeName").html('<h2 id="lastNodeName">'+ select_node["paths"] +' <small>Department Member 部门成员</small></h2>')
				    	  if ($('#structureLastNodesMemberTableLists').hasClass('dataTable')) {
				            dttable = $('#structureLastNodesMemberTableLists').dataTable();
				            dttable.fnClearTable(); //清空table
				            dttable.fnDestroy(); //还原初始化datatable
				    	  }			    	  
				    	  makeMemberTableList(response,select_node)
				    	  /*assets_table_id = select_node["id"]*/
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
	     }
	});	
	
	$('#structureRootTableLists tbody').on('click',"button[name='btn-structure-root-tree']", function(){
    	var vIds = $(this).val();
    	drawTree('#structureTree',requests("get","/api/account/structure/?tree_id="+vIds))
    });		
	
	$('#structureRootTableLists tbody').on('click',"button[name='btn-structure-root-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		let text = td.eq(1).text(); 
    	let desc = td.eq(2).text(); 
    	let manage = td.eq(3).text();
    	let mail_group = td.eq(4).text(); 
    	let wechat_webhook_url = td.eq(5).text(); 	
    	let dingding_webhook_url = td.eq(6).text(); 	

		let selectHtmls = '<select class="form-control"  name="manage" title="上级"><option value="">无</option>'
    	let optionHtml = ''
    	let dataList = requests("get","/api/account/user/")
		for (var i=0; i <dataList.length; i++){
			if (manage==dataList[i]['username'] || manage==dataList[i]['name']){
				optionHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+ dataList[i]['username'] +'</option>' 	
			}else{
				optionHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]['username'] +'</option>' 	
			}
							 
		};   	
		selectHtmls = selectHtmls + optionHtml + '</select>'; 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			               '<input type="text"  name="text" value="'+ text +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +				          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="desc" value="'+ desc +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			            		selectHtmls +
			            '</div>' +
			          '</div>' +			          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">邮件 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="mail_group" value="'+ mail_group +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +			          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">微信<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="wechat_webhook_url" value="'+ wechat_webhook_url +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' + 
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">钉钉 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			               '<input type="text"  name="dingding_webhook_url" value="'+ dingding_webhook_url +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +			          
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	            		var vipForm = this.$content.find('input,select');                	
	            		for (var i = 0; i < vipForm.length; ++i) {
	            			var name =  vipForm[i].name
	            			var value = vipForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};		                	
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/account/structure/nodes/" + vIds + '/',  
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
				                    text: '资产修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshTable('#structureRootTableLists', '/api/account/structure/nodes/');
				            }  
				    	});
	                }
	            }
	        }
	    });	
    });	
	
	
	//删除项目资产
	$('#structureRootTableLists tbody').on('click',"button[name='btn-structure-root-confirm']", function(){
    	var vIds = $(this).val();
    	var projectName = $(this).parent().parent().parent().find("td").eq(1).text()
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除单位: " + projectName,
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/account/structure/nodes/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('#structureRootTableLists', '/api/account/structure/nodes/');		            
	  			      },
	  	              error:function(response){
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: request.responseText,
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
	
    $('#addStructureMemberSubmit').on('click', function() {
		var vIds = $(this).val();
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:'/api/account/structure/nodes/member/'+ vIds + '/',  
            data:$('#addStructureMemberForm').serialize(),
            async: false,  
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
                    text: '用户关联成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable("#structureLastNodesMemberTableLists", '/api/account/structure/nodes/member/'+ vIds + '/')		
            }  
    	});  	
    });	
    
    
})