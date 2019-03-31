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


function InitModelDataTable(tableId,url,buttons,columns,columnDefs){
	  var data = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Bfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	data['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (data['next']){
		  $("button[name='model_page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='model_page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='model_page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='model_page_previous']").attr("disabled", true).val();
	  }
	    
	  
}

function RefreshModelTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList['results'].length; i++)
    {
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
    }

    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='model_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='model_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='model_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='model_page_previous']").attr("disabled", true).val();
    } 
       
  });	
}

function InitPlaybookDataTable(tableId,url,buttons,columns,columnDefs){
	  jobsDataList = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Bfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	jobsDataList['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (jobsDataList['next']){
		  $("button[name='playbook_page_next']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='playbook_page_next']").attr("disabled", true).val();
	  }
	  if (jobsDataList['previous']){
		  $("button[name='playbook_page_previous']").attr("disabled", false).val(jobsDataList['next']);	
	  }else{
		  $("button[name='playbook_page_previous']").attr("disabled", true).val();
	  }	   
}

function RefreshPlaybookLogsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){

    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);
 
    for (var i=0; i<dataList['results'].length; i++){
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
      jobsResults[dataList["results"][i]["id"]] = dataList["results"][i]["result"]
    }
    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='playbook_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='playbook_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='playbook_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='playbook_page_previous']").attr("disabled", true).val();
    }  
    
  });	
}
	
function makePlaybookLogsTableList(dataList){
    var columns = [
                   {"data": "id"},
                   {"data": "ans_user"},
                   {"data": "ans_name"},                  
	               {"data": "ans_content"},
	               {"data": "ans_server"},
	               {"data": "create_time"},
	               ]
   var columnDefs = [     		        
	    		        {
   	    				targets: [6],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-playbook-view" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' +	    	                               	                           
	    	                           '<button type="button" name="btn-playbook-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = [
                   ]    
    InitPlaybookDataTable('deployPlaybookLogTableList','/api/logs/ansible/playbook/',buttons,columns,columnDefs);	
}	

function makeModelLogsTableList(){
    var columns = [                  
                   {"data": "id"},
                   {"data": "ans_user"},
                   {"data": "ans_model"},
                   {"data": "ans_args"},
                   {"data": "ans_server"},
                   {"data": "create_time"},
	               ]
   var columnDefs = [                     
	    		        {
   	    				targets: [6],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +		    	                           
	    	                           '<button type="button" name="btn-model-view" value="'+ row.id +'" class="btn btn-default" data-toggle="modal"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           
	    	                           '<button type="button" name="btn-model-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = []    
    InitModelDataTable('deployModelLogTableList','/api/logs/ansible/model/',buttons,columns,columnDefs);	
}



$(document).ready(function() {	
	
	if($("#deployModelLogTableList").length){

	    $("button[name^='model_page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshModelTable('deployModelLogTableList', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	    makeModelLogsTableList()  
	}		
      
	$('#deployModelLogTableList tbody').on('click',"button[name='btn-model-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(3).text()
		$.confirm({
		    title: '删除确认',
		    content: '确认删除这条日志记录?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/logs/ansible/model/", 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
						RefreshModelTable('deployModelLogTableList', '/api/logs/ansible/model/')											
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
	
	$('#deployModelLogTableList tbody').on('click',"button[name='btn-model-view']",function(){
		var vIds = $(this).val();  
		console.log(vIds)
		let dataList = requests('get','/api/logs/ansible/model/'+ vIds + '/')
		$("#result").html("")
		for(var i=0;i<dataList.length;i++){
			$("#result").append(dataList[i]["content"]+'<br>')
		}
		$("#deployLogsShow").modal('show');
		
    });		
	
	if($("#deployPlaybookLogTableList").length){

	    $("button[name^='playbook_page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshPlaybookLogsTable('deployPlaybookLogTableList', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	    makePlaybookLogsTableList()  
	}	
	
	$('#deployPlaybookLogTableList tbody').on('click',"button[name='btn-playbook-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(3).text()
		$.confirm({
		    title: '删除确认',
		    content: '确认删除这条日志记录?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/logs/ansible/playbook/", 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
						RefreshModelTable('deployPlaybookLogTableList', '/api/logs/ansible/playbook/')											
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
	
	$('#deployPlaybookLogTableList tbody').on('click',"button[name='btn-playbook-view']",function(){
		var vIds = $(this).val();  
		console.log(vIds)
		let dataList = requests('get','/api/logs/ansible/playbook/'+ vIds + '/')
		$("#result").html("")
		for(var i=0;i<dataList.length;i++){
			$("#result").append(dataList[i]["content"]+'<br>')
		}
		$("#deployLogsShow").modal('show');
		
    });		
	
})