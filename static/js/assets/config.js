var userInfo = {
		
}

var envInfo = {
		
}

function makeSelect(ids,key,name,dataList){
	var userHtml = '<select required="required" class="form-control" name="'+ name +'" autocomplete="off">'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option name="'+ name +'"value="'+ dataList[i]["id"] +'">'+ dataList[i][key] +'</option>' 					 
	};                        
	userHtml =  userHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= userHtml;	
}

function getTagsServerList(vIds){
	var iList = []
	var sList = []
	var allAssets = requests('get','/api/assets/')
	for (var i=0; i <allAssets.length; i++){
		sList.push({"id":allAssets[i]["id"],"name":allAssets[i]["detail"]["ip"]})
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
				iList.push({"id":response["data"][i]["id"],"name":response["data"][i]["ip"]})
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

function modfIdc(vIds,idc_name,idc_bandwidth,idc_linkman,idc_phone,idc_address,idc_network,idc_operator,idc_desc){
    $.confirm({
        icon: 'fa fa-edit',
        type: 'blue',
        title: '修改数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房名称<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idc_name" value="'+ idc_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">运营商<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idc_operator" value="'+ idc_operator +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' +		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房带宽<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_idc_bandwidth" value="'+ idc_bandwidth +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' + 		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房联系人<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_idc_linkman" value="'+ idc_linkman +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +   		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">联系人号码<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_idc_phone" value="'+ idc_phone +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' + 
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房地址<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idc_address" value="'+ idc_address +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' + 
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">机房网络<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idc_network" value="'+ idc_network +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' + 	 
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idc_desc" value="'+ idc_desc +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' + 		            
		          '</form>',
        buttons: {
            '取消': function() {},
            '修改': {
                btnClass: 'btn-blue',
                action: function() {
                    var idc_name = this.$content.find("[name='modf_idc_name']").val();
                    var idc_bandwidth = this.$content.find("[name='modf_idc_bandwidth']").val();
                    var idc_linkman = this.$content.find("[name='modf_idc_linkman']").val();
                    var idc_phone = this.$content.find("[name='modf_idc_phone']").val();
                    var idc_address = this.$content.find("[name='modf_idc_address']").val();	
                    var idc_network = this.$content.find("[name='modf_idc_network']").val();	
                    var idc_operator = this.$content.find("[name='modf_idc_operator']").val();	
                    var idc_desc = this.$content.find("[name='modf_idc_desc']").val();	                   
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:"/api/idc/" + vIds + '/',  
			            data:{
			            	"idc_name":idc_name,
			            	"idc_bandwidth":idc_bandwidth,
			            	"idc_phone":idc_phone,
							"idc_linkman":idc_linkman,
							"idc_address":idc_address,
							"idc_network":idc_network,
							"idc_operator":idc_operator,
							"idc_desc":idc_desc,
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
			            	RefreshTable('idcAssetsTable', '/api/idc/');
			            }  
			    	});
                }
            }
        }
    });
}

function modfIdle(vIds,idle_name,idle_number,idle_desc){
    $.confirm({
        icon: 'fa fa-edit',
        type: 'blue',
        title: '修改数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">资产名称<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idle_name" value="'+ idle_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">数量<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_idle_number" value="'+ idle_number +'" required="required"  class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' +		            
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_idle_desc" value="'+ idle_desc +'"  required="required" placeholder="" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' + 		            		            
		          '</form>',
        buttons: {
            '取消': function() {},
            '修改': {
                btnClass: 'btn-blue',
                action: function() {
                    var idle_name = this.$content.find("[name='modf_idle_name']").val();
                    var idle_number = this.$content.find("[name='modf_idle_number']").val();
                    var idle_desc = this.$content.find("[name='modf_idle_desc']").val();                   
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:"/api/idc/idle/" + vIds + '/',  
			            data:{
			            	"idle_name":idle_name,
			            	"idle_number":idle_number,
			            	"idle_desc":idle_desc,
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
			            	RefreshTable('idleAssetsTable', '/api/idc/idle/');
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

function InitDataTable(tableId,dataList,buttons,columns,columnDefs){
//	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				    "dom": "Bfrtip",
				    "buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	dataList,
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

function RefreshUserInfo(){
	var userList = requests("get","/api/user/")
	for (var i=0; i <userList.length; i++){
		userInfo[userList[i]["id"]] = userList[i]
	}		
}

function RefreshEnvInfo(){
	var envList = requests("get","/api/business/env/")
	for (var i=0; i <envList.length; i++){
		envInfo[envList[i]["id"]] = envList[i]
	}		
}

$(document).ready(function() {
		    
	
	function makeTagsTables(dataList){
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
		InitDataTable('tagsAssetsTable',dataList,buttons,columns,columnDefs)			
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
    
	makeTagsTables(requests('get',"/api/tags/"))
	
	
	function makeCabinetTables(dataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "idc_name"},	
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
            	makeSelect("idc_cabinet_select","idc_name","idc",idcList)
            }
        }]
		InitDataTable('cabinetAssetsTable',dataList,buttons,columns,columnDefs)			
	}	
	
    
    $('#cabinetsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/cabinet/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"idc": $('#idc_cabinet_select option:selected').val(),
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
	
	makeCabinetTables(requests('get',"/api/cabinet/"))
	
	function makeRaidTables(dataList){
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
		InitDataTable('raidAssetsTable',dataList,buttons,columns,columnDefs)			
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
	
	makeRaidTables(requests('get',"/api/raid/"))
  
	function makeLineTables(dataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "line_name"},	
	                    {"data": "line_price"},
	                    {"data": "update_time"}
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [4],
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
		InitDataTable('lineAssetsTable',dataList,buttons,columns,columnDefs)			
	}        
	
	$('#lineAssetsTable tbody').on('click',"button[name='btn-line-modf']", function(){
    	var vIds = $(this).val();
    	let line_name = $(this).parent().parent().parent().find("td").eq(1).text(); 
    	let line_price =  $(this).parent().parent().parent().find("td").eq(2).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">线路名称<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="modf_line_name" value="'+ line_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">线路价格<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="modf_line_price" value="'+ line_price +'" required="required"  class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div> ' +		            		            
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    let line_name = this.$content.find("[name='modf_line_name']").val();
	                    let line_price = this.$content.find("[name='modf_line_price']").val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/line/" + vIds + '/',  
				            data:{
				            	"line_name":line_name,
				            	"line_price":line_price
				            },
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
				"line_name": $('#line_name').val(),
				"line_price": $('#line_price').val()
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
	
	makeLineTables(requests('get',"/api/line/"))
	
	function makeGroupTables(dataList){
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
		InitDataTable('groupAssetsTable',dataList,buttons,columns,columnDefs)			
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
	
	makeGroupTables(requests('get',"/api/group/"))
	


	function makeIdcTables(dataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "zone_name"},
	                    {"data": "idc_name"},		
	                    {"data": "idc_operator"},
	                    {"data": "idc_bandwidth"},
	                    {"data": "idc_linkman"},
	                    {"data": "idc_phone"},
	                    {"data": "idc_address"},
	                    {"data": "idc_network"},
	                    {"data": "idc_desc"},
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [10],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-idc-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-idc-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	makeSelect("zone_idc_select","zone_name","zone",zoneList)
            	$('#addIdcModal').modal("show");	
            }
        }]
		InitDataTable('idcAssetsTable',dataList,buttons,columns,columnDefs)			
	}   	
	
	var idcList = requests('get',"/api/idc/")
	
	makeIdcTables(idcList)
	  //修改应用资产
	$('#idcAssetsTable tbody').on('click',"button[name='btn-idc-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var idc_name = td.eq(2).text()
    	var idc_operator = td.eq(3).text()
    	var idc_bandwidth = td.eq(4).text()
    	var idc_linkman = td.eq(5).text()
    	var idc_phone = td.eq(6).text()
    	var idc_address = td.eq(7).text()
    	var idc_network = td.eq(8).text()
    	var idc_desc = td.eq(9).text()
    	modfIdc(vIds,idc_name,idc_bandwidth,idc_linkman,idc_phone,idc_address,idc_network,idc_operator,idc_desc)
    });	
	
	
    $('#idcsubmit').on('click', function() {
    	$.ajax({     		
            cache: true,  
            type: "POST",  
            url:"/api/idc/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"zone": $('#zone_idc_select option:selected').val(),
				"idc_name": $('#idc_name').val(),
				"idc_bandwidth": $('#idc_bandwidth').val(),
				"idc_linkman": $('#idc_linkman').val(),
				"idc_phone": $('#idc_phone').val(),
				"idc_address": $('#idc_address').val(),
				"idc_network": $('#idc_network').val(),
				"idc_operator": $('#idc_operator').val(),
				"idc_desc": $('#idc_desc').val(),
			}),
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
            	RefreshTable('idcAssetsTable', '/api/idc/');
            }  
    	});  	
    });	
	
    
  	//删除机房资产
	$('#idcAssetsTable tbody').on('click',"button[name='btn-idc-confirm']", function(){
    	var vIds = $(this).val();
    	var idcName = $(this).parent().parent().parent().find("td").eq(1).text()
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除机房: " + idcName,
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/idc/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('idcAssetsTable', '/api/idc/');		            
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

	function makeIdleTables(dataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "idc_name"},		
	                    {"data": "idle_name"},
	                    {"data": "idle_number"},
	                    {"data": "idle_username"},
	                    {"data": "idle_desc"},
	                    {"data": "update_time"},
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [7],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-idle-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-idle-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	makeSelect("idc_idle_select","idc_name","idc",idcList)
            	$('#addIdleModal').modal("show");	
            }
        }]
		InitDataTable('idleAssetsTable',dataList,buttons,columns,columnDefs)			
	}   	
	
	var idleList = requests('get',"/api/idc/idle/")
	
	makeIdleTables(idleList)
	
	  //修改应用资产
	$('#idleAssetsTable tbody').on('click',"button[name='btn-idle-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var idle_name = td.eq(2).text()
    	var idle_number = td.eq(3).text()
    	var idle_desc = td.eq(5).text()
    	modfIdle(vIds,idle_name,idle_number,idle_desc)
    });	
	
	
    $('#idlesubmit').on('click', function() {
    	$.ajax({     		
            cache: true,  
            type: "POST",  
            url:"/api/idc/idle/",  
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
				"idc": $('#idc_idle_select option:selected').val(),
				"idle_name": $('#idle_name').val(),
				"idle_number": $('#idle_number').val(),
				"idle_linkman": $('#idle_linkman').val(),
				"idle_desc": $('#idle_desc').val(),
			}),
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
            	RefreshTable('idleAssetsTable', '/api/idc/idle/');
            }  
    	});  	
    });	
	
    
  	//删除机房资产
	$('#idleAssetsTable tbody').on('click',"button[name='btn-idle-confirm']", function(){
    	var vIds = $(this).val();
    	var idleName = $(this).parent().parent().parent().find("td").eq(2).text()
	  	$.confirm({
	  	    title: '删除确认?',
	  	    type: 'red',
	  	    content: "删除机房闲置资产记录: 【" + idleName +"】",
	  	    buttons: {
	  	        确认: function () {
	  			$.ajax({
	  				  type: 'DELETE',
	  				  url:'/api/idc/idle/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('idleAssetsTable', '/api/idc/idle/');		            
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

	function makeZoneTables(dataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "zone_name"},		
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
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
		InitDataTable('zoneAssetsTable',dataList,buttons,columns,columnDefs)			
	}   	
	
	var zoneList = requests('get',"/api/zone/")
	
	makeZoneTables(zoneList)
	
	  //修改应用资产
	$('#zoneAssetsTable tbody').on('click',"button[name='btn-zone-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var zone_name = td.eq(1).text()
        $.confirm({
            icon: 'fa fa-edit',
            type: 'blue',
            title: '修改数据',
            content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
    		            '<div class="form-group">' +
    		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">区域名称<span class="required">*</span>' +
    		              '</label>' +
    		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
    		                '<input type="text"  name="modf_zone_name" value="'+ zone_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
    		              '</div>' +
    		            '</div>' +		            
    		          '</form>',
            buttons: {
                '取消': function() {},
                '修改': {
                    btnClass: 'btn-blue',
                    action: function() {
                        var zone_name = this.$content.find("[name='modf_zone_name']").val();					
    			    	$.ajax({  
    			            cache: true,  
    			            type: "PUT",  
    			            url:"/api/zone/" + vIds + '/',  
    			            data:{
    			            	"zone_name":zone_name,
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
	