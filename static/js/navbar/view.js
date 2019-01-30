function addNavType(){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加导航分类',
        content: '<div class="form-group"><input type="text" value="" placeholder="请输入名称" class="param_name form-control" /></div>',
        buttons: {
            '取消': function() {},
            '添加': {
                btnClass: 'btn-blue',
                action: function() {
                    var param_name = this.$content.find('.param_name').val();
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:"/api/nav/type/",  
			            data:{"type_name":param_name},
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
			            	window.location.reload()
			            }  
			    	});
                }
            }
        }
    });		
}
function addNavTypeSub(vIds){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点名称<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_nav_name" value="" required="required" placeholder="OpsManage" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点描述<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_nav_desc" value="" required="required" placeholder="运维管理平台" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' +
		            '<div class="form-group">' +
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点URL<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text" name="modf_nav_url" value=""  required="required" placeholder="https://github.com/welliamcao/OpsManage" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div>' +                                            			
		          '</form>',
        buttons: {
            '取消': function() {},
            '添加': {
                btnClass: 'btn-blue',
                action: function() {
                    var nav_name = this.$content.find("[name='modf_nav_name']").val();
                    var nav_desc = this.$content.find("[name='modf_nav_desc']").val();
                    var nav_url = this.$content.find("[name='modf_nav_url']").val();
			    	$.ajax({  
			            type: "POST",  
			            url:"/api/nav/number/",  
			            data:{
			            	"nav_type":vIds,
			            	"nav_name":nav_name,
			            	"nav_desc":nav_desc,
			            	"nav_url":nav_url,
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
			            	window.location.reload()
			            }  
			    	});
                }
            }
        }
    });
}

function editNavType(vIds,name){
    $.confirm({
        icon: 'fa fa-edit',
        type: 'blue',
        title: '修改数据',
        content: '<div class="form-group"><input type="text" value="'+ name +'" placeholder="请输入新的名称" class="param_name form-control" /></div>',
        buttons: {
            '取消': function() {},
            '修改': {
                btnClass: 'btn-blue',
                action: function() {
                    var param_name = this.$content.find('.param_name').val();
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:"/api/nav/type/" + vIds + '/',  
			            data:{"type_name":param_name},
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
			            	window.location.reload()
			            }  
			    	});
                }
            }
        }
    });	
}

function deleteNavType(vIds,name){
	$.confirm({
	    title: '删除确认',
	    content:    '确认删除<code><strong>' + name + '</strong></code>类型?<br>注：该操作会删除下面所有导航.',
	    type: 'red',
	    buttons: {
	             删除: function () {		       
			$.ajax({
				url:"/api/nav/type/" + vIds + '/', 
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
	        },			        
	    }
	});	
}

function modfNav(vIds,nav_url,nav_name,nav_desc){
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
		              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">站点描述<span class="required">*</span>' +
		              '</label>' +
		              '<div class="col-md-6 col-sm-6 col-xs-12">' +
		                '<input type="text"  name="modf_nav_desc" value="'+ nav_desc +'" required="required" placeholder="运维管理平台" class="form-control col-md-7 col-xs-12">' +
		              '</div>' +
		            '</div> ' +
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
                    var nav_desc = this.$content.find("[name='modf_nav_desc']").val();
                    var nav_url = this.$content.find("[name='modf_nav_url']").val();
			    	$.ajax({  
			            cache: true,  
			            type: "PUT",  
			            url:"/api/nav/number/" + vIds + '/',  
			            data:{
			            	"nav_name":nav_name,
			            	"nav_url":nav_url,
			            	"nav_desc":nav_desc,
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
			            	window.location.reload()
			            }  
			    	});
                }
            }
        }
    });
}

function deleteNav(vIds,nav_url,nav_name,nav_desc){
	$.confirm({
	    title: '删除确认',
	    content:  '<strong>删除 <code>' + nav_name + '</code>导航？</strong>',
	    type: 'red',
	    buttons: {
	             删除: function () {		       
			$.ajax({
				url:"/api/nav/number/" + vIds + '/', 
				type:"DELETE",  		
				data:{
					"id":vIds,
				}, 
				success:function(response){
//		            window.location.reload();
					RefreshTable('#navbarNumberTbale', '/api/nav/number/')
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

$(document).ready(function() {	
	$.ajax({  
        cache: true,  
        type: "get",  
        url:"/api/nav/type/",  
        async: false,  
        error: function(response) {  
//        	new PNotify({
//                title: 'Ops Failed!',
//                text: request.responseText,
//                type: 'error',
//                styling: 'bootstrap3'
//            });       
        },  
        success: function(response) { 
        	if (response.length > 0){
            	var bavbarTags = ''       	
            		for (var i = 0; i < response.length; ++i) {
            			var bavbarDivs = '';
            			for (var x = 0; x < response[i]["nav_type_number"].length; ++x) {
            				bavbarDivs += '<div class="col-sm-3">' +
        	    							 '<div class="xe-widget xe-conversations box2 label-info" onclick=\'window.open("'+  response[i]["nav_type_number"][x]["nav_url"] +'", "_blank")\' data-toggle="tooltip" data-placement="bottom" title="" data-original-title="'+  response[i]["nav_type_number"][x]["nav_url"] +'">' +
        					                    '<div class="xe-comment-entry" title="'+ response[i]["nav_type_number"][x]["id"] +'">' +
        					                        '<a class="xe-user-img">' +
        					                            '<img src="/nav/'+  response[i]["nav_type_number"][x]["nav_img"].replace("/navbar", "") +'" class="img-circle" width="40">' +
        					                        '</a>' +
        					                        '<div class="xe-comment">' +
        					                            '<a href="/assets/list" class="xe-user-name overflowClip_1">' +
        					                                '<strong>'+  response[i]["nav_type_number"][x]["nav_name"] +'</strong>' +
        					                            '</a>' +
        					                            '<p class="overflowClip_2">'+  response[i]["nav_type_number"][x]["nav_desc"] +'</p>' +
        					                        '</div>' +
        					                     '</div>' +
        					                   '</div>' +
        				                   '</div>'   
            			}    			
            			bavbarTags += '<br>' +
        	             '<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="common-'+ response[i]['id'] +'"></i>'+  response[i]['type_name'] +'</h4>' +
        	             '<div class="row">' +	                
        	                	bavbarDivs +	                
        	             '</div>'
            		}
                	$('#navbarList').html(bavbarTags)
                	$(function () { $("[data-toggle='tooltip']").tooltip(); }); 
                	$.contextMenu({
                        selector: '.xe-comment-entry',
                        callback: function(key, options) {                   
                           var nav_url = $(this).parent().attr('data-original-title')
                           var vIds = $(this).attr('title')
                           var nav_name = $(this).find('strong').text()
                           var nav_desc = $(this).find('p').text()
                           if (key=="edit"){
                        	   modfNav(vIds,nav_url,nav_name,nav_desc)
                           }
                           else if(key=="delete"){
                        	   deleteNav(vIds,nav_url,nav_name,nav_desc)
                           }
                           
                        },
                        items: {
                            "edit": {name: "编辑", icon: "fa-edit"},
                            "delete": {name: "删除", icon: "fa-trash"},
                        }
                    });
                	$.contextMenu({
                        selector: '.text-gray',
                        callback: function(key, options) {      
                        	var vIds = $(this).find('i').attr('id').replace("common-", "")  
                        	var name = $(this).text()
                        	if(key=="addNavType"){
                        		addNavTypeSub(vIds)
                        	}
                        	else if(key=="editNavType"){
                        		editNavType(vIds,name)
                        	}
                        	else if (key=="deleteNavType"){
                        		deleteNavType(vIds,name)                        		
                        	}
                        },
                        items: {
                        	"addNavType": {name: "添加", icon: "fa-plus"},
                            "editNavType": {name: "编辑", icon: "fa-edit"},
                            "deleteNavType": {name: "删除", icon: "fa-trash"},
                        }
                    });                 	
        	}

        }  
	});	

	$.contextMenu({
        selector: '.text-primary',
        callback: function(key, options) {      
        	addNavType()
        },
        items: {
        	"add": {name: "添加", icon: "fa-plus"},
        }
    });  	
	
})