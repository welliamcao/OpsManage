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

function getSelectValue(id){
    var select = document.getElementById(id);
    var val = [];
    for(i=0;i<select.length;i++){
        if(select.options[i].selected){
        	val.push(select[i].value); 
        }
    }
    return val;
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

function makeSelect(name,dataList){
	var binlogHtml = '<select class="selectpicker" name="'+name+'" id="select_'+ name +'" data-live-search="true" data-size="10" data-selected-text-format="count > 3"  data-width="100%" autocomplete="off"  required>'
	var selectHtml = '';
	for (var i=0; i < dataList.length; i++){
		 selectHtml += '<option name="'+name+'" value="'+ dataList[i]["id"] +'">' + dataList[i]["name"] + '</option>' 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById('select_'+name).innerHTML= binlogHtml;	
	$('.selectpicker').selectpicker('refresh');
//	$("#select_"+name).html(binlogHtml)
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
	  
	  makeSelect(tableId.replace("TableLists", ""),data)
}

function RefreshTable(tableId, urlData)
{
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
    makeSelect(tableId.replace("TableLists", ""),dataList)
  });
}

function addCategory(){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加WIKI分类',
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
			            url:"/api/wiki/category/",  
			            data:{"name":param_name},
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
			                    text: '添加成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable("categoryTableLists", "/api/wiki/category/")
			            }  
			    	});
                }
            }
        }
    });	
}

function addTag(){
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加WIKI标签',
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
			            url:"/api/wiki/tag/",  
			            data:{"name":param_name},
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
			                    text: '添加成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable("tagTableLists", "/api/wiki/tag/")
			            }  
			    	});
                }
            }
        }
    });	
}

CKEDITOR.replace('content', {
	   filebrowserUploadUrl: '/wiki/upload/',
	   height: '500px',
	   width: '100%',
});	
$(document).ready(function() {
	function makeCategoryTableLists(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "name"},			                
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-category-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-category-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	addCategory()
            }
        }]
		InitDataTable('categoryTableLists',"/api/wiki/category/",buttons,columns,columnDefs)
	}	  
	makeCategoryTableLists()
	
	$('#categoryTableLists tbody').on('click','button[name="btn-category-edit"]',function(){
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
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
				            url:"/api/wiki/category/" + vIds + '/',  
				            data:{"name":param_name},
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
				            	RefreshTable("categoryTableLists", "/api/wiki/category/")
				            }  
				    	});
	                }
	            }
	        }
	    });   		
	});	
	
	$('#categoryTableLists tbody').on('click','button[name="btn-category-delete"]',function(){
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
		$.confirm({
		    title: '删除确认',
		    content:    '注：该操作会删除<strong>[<code>'+ name +'</code>]</strong>下面所有文章.',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
					$.ajax({
						url:"/api/wiki/category/" + vIds + '/',  
						type:"DELETE",  		
						data:{
							"id":vIds,
						}, 
						success:function(response){
							RefreshTable("categoryTableLists", "/api/wiki/category/")
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
	
	function makeTagsTableLists(){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "name"},			                
		               ]
	    var columnDefs = [								
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-tag-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-tag-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	addTag()
            }
        }]
		InitDataTable('tagTableLists',"/api/wiki/tag/",buttons,columns,columnDefs)
	}
	makeTagsTableLists()
	
	$('#tagTableLists tbody').on('click','button[name="btn-tag-edit"]',function(){
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
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
				            url:"/api/wiki/tag/" + vIds + '/',  
				            data:{"name":param_name},
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
				            	RefreshTable("tagTableLists", "/api/wiki/tag/")
				            }  
				    	});
	                }
	            }
	        }
	    });   		
	});	
	
	$('#tagTableLists tbody').on('click','button[name="btn-tag-delete"]',function(){
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(1).text();
		$.confirm({
		    title: '删除确认',
		    content:    '注：该操作会删除<strong>[<code>'+ name +'</code>]</strong>下面所有文章.',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
					$.ajax({
						url:"/api/wiki/tag/" + vIds + '/',  
						type:"DELETE",  		
						data:{
							"id":vIds,
						}, 
						success:function(response){
							RefreshTable("tagTableLists", "/api/wiki/tag/")
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
	
    $("button[name='addWiki']").on("click", function(){
		tags = getSelectValue("select_tag")
		if (tags.length == 0){
        	new PNotify({
                title: 'Ops Failed!',
                text: "标签类型不能为空",
                type: 'error',
                styling: 'bootstrap3'
            });
			return false;
		};    	
		$.ajax({
			dataType: "JSON",
			url:'/wiki/add/', //请求地址
			type:"POST",  //提交类似
			data:{
				"title":$("#title").val(),
				"content":CKEDITOR.instances.content.getData(),
				"tag": tags,
				"category": $('#select_category option:selected').val(),
			}, //提交参数
			success:function(response){
                if (response["code"]=="200"){ 
/*	            	new PNotify({
	                    title: 'Success!',
	                    text: '修改成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });  */              	
                 	location.reload(); 
                }
	        	else{
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                });  
	        	};					
			},
	    	error:function(response){
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });  
	    	}
		})	    	
    })
	
	
});

	