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
		    		"autoWidth": true	    			
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


function makeNavbarThirdTableList(){
    var columns = [
                   {"data": "id"},
	               {"data": "type_name"},
	               {"data": "icon"},
	               ]
   var columnDefs = [									
	    		        {
   	    				targets: [3],
   	    				render: function(data, type, row, meta) {
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-navbar-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-info"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +		                				                            		                            			                          
	    	                           '<button type="button" name="btn-navbar-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
        	$('#addNavbarThirdModal').modal("show")
        }
    }]
	InitDataTable('navbarThirdTbale','/api/nav/third/',buttons,columns,columnDefs);	
}	

function makeNavbarThirdNumberTableList(){
    var columns = [
                   {"data": "id"},
                   {"data": "type_name"},
	               {"data": "nav_name"},
	               {"data": "width"},
	               {"data": "height"},
	               {"data": "url"},
	               ]
   var columnDefs = [									
	    		        {
   	    				targets: [6],
   	    				render: function(data, type, row, meta) {
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-navbarnumber-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-info"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +		                				                            		                            			                          
	    	                           '<button type="button" name="btn-navbarnumber-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
        	var dataList =  requests('get','/api/nav/third/')
    		var selectHtml = '';
    		var binlogHtml = '<select class="form-control" name="selectpicker form-control" id="navbar_select"   required>'
    		for (var i = 0; i < dataList.length; ++i) {
    			selectHtml += '<option name="type_id" value="'+ dataList[i]["id"] +'">' + dataList[i]["type_name"] + '</option>' 	                								
    		}
    		binlogHtml =  binlogHtml + selectHtml + '</select>'; 
    		$("#navbar_select").html(binlogHtml);
    		$('.selectpicker').selectpicker('refresh');	        	
        	$('#addNavbarThirdNumberModal').modal("show")
        }
    }]    
	InitDataTable('navbarThirdNumberTbale','/api/nav/third/number/',buttons,columns,columnDefs);	
}	

$(document).ready(function() {	
	
	makeNavbarThirdTableList()
	
	makeNavbarThirdNumberTableList()
	
	//添加项目资产
    $('#navbarsubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/nav/third/",  
            data:$('#navbarform').serialize(),
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
            	RefreshTable('#navbarThirdTbale', '/api/nav/third/')
            }  
    	});  	
    });	
	$('#navbarThirdTbale tbody').on('click',"button[name='btn-navbar-edit']",function(){
    	var vIds = $(this).val();
    	var type_name = $(this).parent().parent().parent().find("td").eq(1).text(); 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">类型名称 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="modf_type_name" value="'+ type_name +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">图标类型<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
	                        '<select class="form-control" data-live-search="true" name="modf_icon"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  autocomplete="off" >' +	
									'<option value="fa fa-arrows">arrows</option>' +
									'<option value="fa fa-anchor">anchor</option>' +   
									'<option value="fa fa-cloud">cloud</option>' + 
									'<option value="fa fa-tachometer">tachometer</option>' + 
									'<option value="fa fa-search-plus">search-plus</option>' + 
									'<option value="fa fa-shopping-cart">shopping-cart</option>' + 
									'<option value="fa fa-users">users</option>' + 
									'<option value="fa fa-signal">signal</option>' + 
									'<option value="fa fa-plug">plug</option>' + 
									'<option value="fa fa-gavel">gavel</option>' + 
									'<option value="fa fa-folder-open">folder-open</option>' + 
									'<option value="fa fa-database">database</option>' + 
									'<option value="fa fa-cloud-download">cloud-download</option>' +                        		
			                  '</select>' +
			            '</div>' +
			          '</div>' + 		                        
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find("[name='modf_type_name']").val();
	                    var icon = this.$content.find('select option:selected').val();
	                    console.log(icon,param_name)
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/nav/third/" + vIds + '/',  
				            data:{
				            		"type_name":param_name,
				            		"icon":icon
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
				            	RefreshTable('#navbarThirdTbale', '/api/nav/third/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	
	
	
	
    $('#navbarnumbersubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/nav/third/number/", 
			contentType : "application/json", 
			dataType : "json", 
			data:JSON.stringify({
            	"nav_third_id":$('#navbar_select option:selected').val(),
            	"nav_name":$('#nav_name').val(),
            	"width":$('#nav_width').val(),
            	"height":$('#nav_height').val(),
            	"url":$('#nav_url').val(),
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
            	RefreshTable('#navbarThirdNumberTbale', '/api/nav/third/number/')
            }  
    	});  	
    });    
    
	$('#navbarThirdNumberTbale tbody').on('click',"button[name='btn-navbarnumber-edit']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var nav_name =  td.eq(2).text()
    	var nav_width =  td.eq(3).text()
    	var nav_height =  td.eq(4).text()
    	var nav_url =  td.eq(5).text()
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点名称<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text"  name="modf_nav_name" value="'+ nav_name +'" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">宽度<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="modf_nav_width" value="'+ nav_width +'"  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">高度<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="modf_nav_height" value="'+ nav_height +'"  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 	
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点URL<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			                '<input type="text" name="modf_nav_url" value="'+ nav_url +'"  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
			              '</div>' +
			            '</div>' + 			            
			          '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var nav_name = this.$content.find("[name='modf_nav_name']").val();
	                    var nav_width = this.$content.find("[name='modf_nav_width']").val();
	                    var nav_height = this.$content.find("[name='modf_nav_height']").val();
	                    var nav_url = this.$content.find("[name='modf_nav_url']").val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/nav/third/number/" + vIds + '/',  
							contentType : "application/json", 
							dataType : "json", 
							data:JSON.stringify({
				            	"nav_name":nav_name,
				            	"width":nav_width,
				            	"height":nav_height,
				            	"url":nav_url,
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
				                    text: '修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshTable('#navbarThirdNumberTbale', '/api/nav/third/number/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	
	
	$('#navbarThirdNumberTbale tbody').on('click',"button[name='btn-navbarnumber-delete']",function(){
		var vIds = $(this).val();  
		var type = $(this).parent().parent().parent().find("td").eq(1).text()
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content:    "【" + type +"】" + '<strong> <code>' + name + '</code></strong>站点',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:"/api/nav/third/number/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
//			            window.location.reload();
						RefreshTable('#navbarThirdNumberTbale', '/api/nav/third/number/')
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
	
	$('#navbarThirdTbale tbody').on('click',"button[name='btn-navbar-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content:    '确认删除<code><strong>' + name + '</strong></code>类型?',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:"/api/nav/third/" + vIds + '/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
//			            window.location.reload();
						RefreshTable('#navbarThirdTbale', '/api/nav/third/')
						RefreshTable('#navbarThirdNumberTbale', '/api/nav/third/number/')
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