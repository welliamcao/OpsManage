var userInfo = {
		
}

function getTagsServerList(vIds){
	var iList = []
	var sList = []
	var allAssets = requests('get','/api/assets/')
	for (var i=0; i <allAssets.length; i++){
		sList.push({"id":allAssets[i]["id"],"name":allAssets[i]["project"]+' | '+allAssets[i]["service"]+' | '+allAssets[i]["detail"]["ip"]})
	}
	$.ajax({  
        cache: true,  
        type: "POST",    
        url:"/assets/server/query/",  
        data:{
        	"query":'tags',
        	"id":vIds
        },
        async: false,  
        error: function(response) {
        	iList = []
        	new PNotify({
                title: 'Ops Failed!',
                text: response.responseText,
                type: 'error',
                styling: 'bootstrap3'
            });       
        },  
        success: function(response) {  	
			for (var i=0; i <response["data"].length; i++){
				iList.push({"id":response["data"][i]["id"],"name":response["data"][i]["project"]+' | '+response["data"][i]["service"]+' | '+response["data"][i]["ip"]})
				for (var j=0; j <sList.length; j++){
					if(sList[j]["id"]==response["data"][i]["id"]){
						sList.splice(j, 1);
					}
				}
			}				
        }  
	});	 
	return {"tags":iList,"all":sList}
}

function modfZone(vIds,zone_name,zone_network,zone_local,zone_contact,zone_number){
    $.confirm({
        icon: 'fa fa-edit',
        type: 'blue',
        title: '修改数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房名称<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_zone_name" value="'+ zone_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房联系人<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_zone_contact" value="'+ zone_contact +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' + 		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房位置<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_zone_local" value="'+ zone_local +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +   		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">联系人号码<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_zone_number" value="'+ zone_number +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' + 
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房网段<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_zone_network" value="'+ zone_network +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' + 		            
		          '</form>',
        buttons: {
            '取消': function() {},
            '修改': {
                btnClass: 'btn-blue',
                action: function() {
                    var zone_name = this.$content.find("[name='modf_zone_name']").val();
                    var zone_network = this.$content.find("[name='modf_zone_network']").val();
                    var zone_local = this.$content.find("[name='modf_zone_local']").val();
                    var zone_contact = this.$content.find("[name='modf_zone_contact']").val();
                    var zone_number = this.$content.find("[name='modf_zone_number']").val();					
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:"/api/zone/" + vIds + '/',  
			            data:{
			            	"zone_name":zone_name,
			            	"zone_local":zone_local,
			            	"zone_network":zone_network,
							"zone_contact":zone_contact,
							"zone_number":zone_number,
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
			                    text: '修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('zoneAssetsTable', '/api/zone/');
			            }  
			    	});
                }
            }
        }
    });
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

function RefreshTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList )
	{
	  table = $('#'+tableId).dataTable();
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

$(function(){
	var userList = requests("get","/api/user/")
	for (var i=0; i <userList.length; i++){
		userInfo[userList[i]["id"]] = userList[i]
	}		
})

$(document).ready(function() {
	
	function makeProjectsTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "project_name"},	
	                    {"data": "project_owner"},
		               ]
	    var columnDefs = [	
	   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {	
	    	                        return userInfo[row.project_owner]["username"]
	    	    				},
	    	    				"className": "text-center",
   	    		        },	                      
   	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-project-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-project-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addProjectModal').modal("show");	
            	var userList = requests("get","/api/user/")
				var userHtml = '<select required="required" class="form-control" name="project_owner" id="project_owner"  autocomplete="off">'
				var selectHtml = '';
				for (var i=0; i <userList.length; i++){
					selectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 					 
				};                        
				userHtml =  userHtml + selectHtml + '</select>';
				document.getElementById("project_owner").innerHTML= userHtml;								            	
            }
        }]
		InitDataTable('projectTableLists',"/api/project/",buttons,columns,columnDefs)			
	}  	
    
	makeProjectsTables()
	

  //修改项目资产
	$('#projectTableLists tbody').on('click',"button[name='btn-project-modf']", function(){
    	var vIds = $(this).val();
		var project = $(this).parent().parent().parent().find("td").eq(1).text(); 
		var username = $(this).parent().parent().parent().find("td").eq(2).text(); 
    	var userList = requests("get","/api/user/")
		var userHtml = '<select required="required" class="form-control"  autocomplete="off">'
		var selectHtml = '';
		for (var i=0; i <userList.length; i++){
			if (userList[i]["username"]==username){
				selectHtml += '<option selected="selected" value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 	
			}else{
				selectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 	
			}
							 
		};                        
		userHtml =  userHtml + selectHtml + '</select>';		
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">项目名称 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="project_name" value="'+ project +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">项目负责人<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              userHtml +
			            '</div>' +
			          '</div>' + 		                        
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find("[name='project_name']").val();
	                    var project_owner = this.$content.find('select option:selected').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/project/" + vIds + '/',  
				            data:{
				            	"project_name":param_name,
				            	"project_owner":project_owner
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
				                    text: '资产修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshTable('projectTableLists', '/api/project/');
				            }  
				    	});
	                }
	            }
	        }
	    });	
/*    	$.ajax({  
            cache: true,  
            type: "PUT",  
			contentType : "application/json", 
			dataType : "json", 	            
            url:"/api/project/" + vIds + '/',  
            data:JSON.stringify({
				"project_owner": $('#project_owner_' + vIds + ' option:selected').val(),
				"project_name": $('#project_name_' + vIds).val(),
			}),
            async: false,  
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
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
            	RefreshTable('projectTableLists', '/api/project/');
            }  
    	}); */ 	
    });	
	
	
	//删除项目资产
	$('#projectTableLists tbody').on('click',"button[name='btn-project-confirm']", function(){
    	var vIds = $(this).val();
    	var projectName = $(this).parent().parent().parent().find("td").eq(1).text()
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除项目: " + projectName,
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/project/' + vIds + '/',
	  			      success:function(response){	
	  			    	$.alert('删除成功!');			            
	  			      },
	  	              error:function(response){
	  	            	$.alert('删除失败!');		
	  	              }
	  				});	        
	  	        },
	  	       	 取消: function () {
	  	            return true;
	  	        },
	  	    }
	  	});   
    });	
    
	//添加项目资产
    $('#projectsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/project/",  
            data:$('#projectAssetsform').serialize(),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('projectTableLists', '/api/project/');
            }  
    	});  	
    });		
	
	function makeServiceTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "project_name"},		
	                    {"data": "service_name"},	
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-service-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-service-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addServiceModal').modal("show");	
            	var projectList = requests("get","/api/project/")
				var userHtml = '<select required="required" class="form-control" id="project_service_select"  autocomplete="off">'
				var selectHtml = '';
				for (var i=0; i <projectList.length; i++){
					selectHtml += '<option value="'+ projectList[i]["id"] +'">'+ projectList[i]["project_name"] +'</option>' 					 
				};                        
				userHtml =  userHtml + selectHtml + '</select>';
				document.getElementById("project_service_select").innerHTML= userHtml;	            	
            }
        }]
		InitDataTable('serviceAssetsTable',"/api/service/",buttons,columns,columnDefs)			
	}
	
    $('#servicesubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/service/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"project_id": $('#project_service_select option:selected').val(),
				"project_name": $('#project_service_select option:selected').text(),
				"service_name": $('#service_name').val()
			}),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('serviceAssetsTable', '/api/service/');
            }  
    	});  	
    });		

	$('#serviceAssetsTable tbody').on('click',"button[name='btn-service-modf']", function(){
    	var vIds = $(this).val();
    	var service = $(this).parent().parent().parent().find("td").eq(2).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" value="'+service+'" placeholder="请输入新的应用名称" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/service/" + vIds + '/',  
				            data:{"service_name":param_name},
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
				            	RefreshTable('serviceAssetsTable', '/api/service/');
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	 
	
    $('#serviceAssetsTable tbody').on('click',"button[name='btn-service-confirm']", function(){
      	var vIds = $(this).val();
      	var service = $(this).parent().parent().parent().find("td").eq(2).text(); 
    	$.confirm({
    	    title: '删除确认?',
    	    type: 'red',
    	    content: "删除应用: <code>" + service +'</code>',
    	    buttons: {
    	        确认: function () {
	    			$.ajax({
	    				  type: 'DELETE',
	    				  url:'/api/service/' + vIds + '/',
	    			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
	    			    	RefreshTable('serviceAssetsTable', '/api/service/');
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
	
	makeServiceTables()
	
	function makeTagsTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "tags_name"},		
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-tags-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 
		    	                           '<button type="button" name="btn-tags-group" value="'+ row.id +'" class="btn btn-default" data-toggle="modal" data-target=".bs-example-modal-tags-info"><span class="fa fa-group" aria-hidden="true"></span>' +	
		    	                           '</button>' +		    	                           
		    	                           '<button type="button" name="btn-tags-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addTagsModal').modal("show");	
            }
        }]
		InitDataTable('tagsAssetsTable',"/api/tags/",buttons,columns,columnDefs)			
	}	
	
	$('#tagsAssetsTable tbody').on('click',"button[name='btn-tags-group']", function(){
    	var vIds = $(this).val();
    	var tagsName = $(this).parent().parent().parent().find("td").eq(1).text(); 
    	$("#taggroupsubmit").val(vIds)
    	$("#myTagsModalLabel").html('<h4 class="modal-title" id="myModalLabel"><code>'+ tagsName +'</code>标签分类</h4>')
    	$('select[name="doublebox"]').empty();
    	var data = getTagsServerList(vIds)
		$('select[name="doublebox"]').doublebox({
	        nonSelectedListLabel: '选择主机资产',
	        selectedListLabel: '已分配资产',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["tags"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	    	
    	
    });	   
    
    $("#taggroupsubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
				contentType : "application/json", 
				dataType : "json", 	            
	            url:"/api/tags/assets/"+vIds+'/',  
	            data:JSON.stringify({
					"ids": vServer
				}),
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
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
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

	  //修改使用组资产
    $('#tagsAssetsTable tbody').on('click',"button[name='btn-tags-modf']", function(){
    	var vIds = $(this).val();
    	var tagsName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" value="'+tagsName+'" placeholder="请输入新的名称" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/tags/" + vIds + '/',  
				            data:{"tags_name":param_name},
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
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
				            	RefreshTable('tagsAssetsTable', '/api/tags/');		
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	    
    
  	//删除Tags资产  
    $('#tagsAssetsTable tbody').on('click',"button[name='btn-tags-confirm']", function(){
    	var vIds = $(this).val();
    	var tagsName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除标签: 【" + tagsName +'】',
	  	    buttons: {
	  	       确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/tags/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
	    			    	RefreshTable('tagsAssetsTable', '/api/tags/');		            
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
    
    $('#tagssubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/tags/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"tags_name": $('#tag_name').val(),
			}),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('tagsAssetsTable', '/api/tags/');
            }  
    	});  	
    });	    
    
	makeTagsTables()
	
	
	function makeCabinetTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "zone_name"},	
	                    {"data": "cabinet_name"},	
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-cabinet-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-cabinet-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addCabinetModal').modal("show");	
            }
        }]
		InitDataTable('cabinetAssetsTable',"/api/cabinet/",buttons,columns,columnDefs)			
	}	
	
    
    $('#cabinetsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/cabinet/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"zone_id": $('#zone_cabinet_select option:selected').val(),
				"zone_name": $('#zone_cabinet_select option:selected').text(),
				"cabinet_name": $('#cabinet_name').val()
			}),
            async: false,  
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });       
            },  
            success: function(data) {  
            	new PNotify({
                    title: 'Success!',
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('cabinetAssetsTable', '/api/cabinet/');
            }  
    	});  	
    });	    
    
    $('#cabinetAssetsTable tbody').on('click',"button[name='btn-cabinet-modf']", function(){
    	var vIds = $(this).val();
    	var cabinetName = $(this).parent().parent().parent().find("td").eq(2).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" value="'+cabinetName+'" placeholder="请输入新的应用名称" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/cabinet/" + vIds + '/',  
				            data:{"cabinet_name":param_name},
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
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
				            	RefreshTable('cabinetAssetsTable', '/api/cabinet/');	
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	    

  	//删除机柜资产  
    $('#cabinetAssetsTable tbody').on('click',"button[name='btn-cabinet-confirm']", function(){
    	var vIds = $(this).val();
    	var cabinetName = $(this).parent().parent().parent().find("td").eq(2).text(); 
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除机柜: " + cabinetName,
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/cabinet/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
	    			    	RefreshTable('cabinetAssetsTable', '/api/cabinet/');		            
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
	
	makeCabinetTables()
	
	function makeRaidTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "raid_name"},		
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-raid-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-raid-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addRaidModal').modal("show");	
            }
        }]
		InitDataTable('raidAssetsTable',"/api/raid/",buttons,columns,columnDefs)			
	}	
	
    $('#raidsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/raid/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"raid_name": $('#raid_name').val(),
			}),
            async: false,  
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });       
            },  
            success: function(data) {  
            	new PNotify({
                    title: 'Success!',
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('raidAssetsTable', '/api/raid/');
            }  
    	});  	
    });		
	
	$('#raidAssetsTable tbody').on('click',"button[name='btn-raid-modf']", function(){
    	var vIds = $(this).val();
    	var raidName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" value="'+raidName+'" placeholder="请输入新的名称" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/raid/" + vIds + '/',  
				            data:{"raid_name":param_name},
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
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
				            	RefreshTable('raidAssetsTable', '/api/raid/');
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	 
	
	$('#raidAssetsTable tbody').on('click',"button[name='btn-raid-confirm']", function(){
    	var vIds = $(this).val();
    	var raidName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除Raid: " + raidName,
	  	    buttons: {
	  	         确认: function () {
	  				$.ajax({
	  					  type: 'DELETE',
	  					  url:'/api/raid/' + vIds + '/',
	  				      success:function(response){	
				            	new PNotify({
				                    title: 'Success!',
				                    text: '资产修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshTable('raidAssetsTable', '/api/raid/');		            
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
	
	makeRaidTables()
  
	function makeLineTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "line_name"},		
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-line-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-line-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addLineModal').modal("show");	
            }
        }]
		InitDataTable('lineAssetsTable',"/api/line/",buttons,columns,columnDefs)			
	}        
	
	$('#lineAssetsTable tbody').on('click',"button[name='btn-line-modf']", function(){
    	var vIds = $(this).val();
    	var lineName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" VALUE="'+ lineName +'" placeholder="请输入新的出口线路" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/line/" + vIds + '/',  
				            data:{"line_name":param_name},
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
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
				            	RefreshTable('lineAssetsTable', '/api/line/');	
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	
	
	$('#lineAssetsTable tbody').on('click',"button[name='btn-line-confirm']", function(){
  	  	var vIds = $(this).val();
  	  	var lineName = $(this).parent().parent().parent().find("td").eq(1).text(); 
  		$.confirm({
  		    title: '删除确认?',
  		    type: 'red',
  		    content: "删除项目: " + lineName,
  		    buttons: {
  		        确认: function () {
  				$.ajax({
  					  type: 'DELETE',
  					  url:'/api/line/' + vIds + '/',
  				      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('lineAssetsTable', '/api/line/');			            
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
	
    $('#linesubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/line/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"line_name": $('#line_name').val()
			}),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('lineAssetsTable', '/api/line/');	
            }  
    	});  	
    });		
	
	makeLineTables()
	
	function makeGroupTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "name"},		
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-group-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-group-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addGroupModal').modal("show");	
            }
        }]
		InitDataTable('groupAssetsTable',"/api/group/",buttons,columns,columnDefs)			
	}  	
	
	  //修改使用组资产
	$('#groupAssetsTable tbody').on('click',"button[name='btn-group-modf']", function(){
    	var vIds = $(this).val();
    	var groupName = $(this).parent().parent().parent().find("td").eq(1).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<div class="form-group"><input type="text" value="'+groupName+'" placeholder="请输入新的名称" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/group/" + vIds + '/',  
				            data:{"name":param_name},
				            error: function(response) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: response.responseText,
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
				            	RefreshTable('groupAssetsTable', '/api/group/');	
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	
	
  	//删除Group资产  
	$('#groupAssetsTable tbody').on('click',"button[name='btn-group-confirm']", function(){
    var vIds = $(this).val();
    var groupName = $(this).parent().parent().parent().find("td").eq(1).text(); 
  	$.confirm({
  	    title: '删除确认?',
  	    type: 'red',
  	    content: "删除使用组: " + groupName,
  	    buttons: {
  	        确认: function () {
  			$.ajax({
  				  type: 'DELETE',
  				  url:'/api/group/' + vIds + '/',
  			      success:function(response){	
		            	new PNotify({
		                    title: 'Success!',
		                    text: '资产删除成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	RefreshTable('groupAssetsTable', '/api/group/');		            
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
	
    $('#groupsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/group/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"name": $('#group_name').val()
			}),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('groupAssetsTable', '/api/group/');	
            }  
    	});  	
    });		
	
	makeGroupTables()
	
  //修改应用资产

	function makeZoneTables(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "zone_name"},		
	                    {"data": "zone_contact"},
	                    {"data": "zone_local"},
	                    {"data": "zone_number"},
	                    {"data": "zone_network"},
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [6],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-zone-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-zone-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addZoneModal').modal("show");	
            }
        }]
		InitDataTable('zoneAssetsTable',"/api/zone/",buttons,columns,columnDefs)			
	}   	
	
	makeZoneTables()
	  //修改应用资产
	$('#zoneAssetsTable tbody').on('click',"button[name='btn-zone-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var zone_name = td.eq(1).text()
    	var zone_contact = td.eq(2).text()
    	var zone_local = td.eq(3).text()
    	var zone_number = td.eq(4).text()
    	var zone_network = td.eq(5).text()
    	console.log(zone_name,zone_network)
    	modfZone(vIds,zone_name,zone_network,zone_local,zone_contact,zone_number)
    });	
	
	
    $('#zonesubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/zone/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"zone_name": $('#zone_name').val(),
				"zone_network": $('#zone_network').val(),
				"zone_local": $('#zone_local').val(),
				"zone_contact": $('#zone_contact').val(),
				"zone_number": $('#zone_number').val(),
			}),
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
                    text: '资产添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshTable('zoneAssetsTable', '/api/zone/');
            }  
    	});  	
    });	
	
    
  	//删除机房资产
	$('#zoneAssetsTable tbody').on('click',"button[name='btn-zone-confirm']", function(){
    	var vIds = $(this).val();
    	var zoneName = $(this).parent().parent().parent().find("td").eq(1).text()
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除机房: " + zoneName,
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/zone/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('zoneAssetsTable', '/api/zone/');		            
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
	