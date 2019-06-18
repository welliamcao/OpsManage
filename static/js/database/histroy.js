var sqlHistroyResults = {}
var sqlHistroyDataList = []
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

function InitSQLHistroyDataTable(tableId,url,buttons,columns,columnDefs){
	  sqlHistroyDataList = requests('get',url)
	  oOverviewTable =$('#'+tableId).dataTable(
			  {
				  	"dom": "Bfrtip",
				  	"buttons":buttons,
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,	
		    		"destroy": true, 
		    		"data":	sqlHistroyDataList['results'],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (sqlHistroyDataList['next']){
		  $("button[name='page_next']").attr("disabled", false).val(sqlHistroyDataList['next']);	
	  }else{
		  $("button[name='page_next']").attr("disabled", true).val();
	  }
	  if (sqlHistroyDataList['previous']){
		  $("button[name='page_previous']").attr("disabled", false).val(sqlHistroyDataList['next']);	
	  }else{
		  $("button[name='page_previous']").attr("disabled", true).val();
	  }	    	 	  
}

function RefreshSQLHistroyDataTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
    table = $('#'+tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList['results'].length; i++){
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
      sqlHistroyResults[dataList["results"][i]["id"]] = dataList["results"][i]["exe_sql"]
    }

    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='page_previous']").attr("disabled", true).val();
    } 
            
  });	
}

function AutoReload(tableId,url){
  RefreshTable('#'+tableId, url);
  setTimeout(function(){AutoReload(url);}, 30000);
}

function getFormatDate(time){  
    var nowDate = new Date(new Date()-1000*time);   
    var year = nowDate.getFullYear();  
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;  
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();  
    var hour = nowDate.getHours()< 10 ? "0" + nowDate.getHours() : nowDate.getHours();  
    var minute = nowDate.getMinutes()< 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();  
    var second = nowDate.getSeconds()< 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds();  
    return year + "-" + month + "-" + date+" "+ hour + ":" + minute + ":" + second;  
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


$(document).ready(function() {
	
	$(function(){
		$.ajax({
			dataType: "JSON",
			url:'/db/manage/?type=query_user_db', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="db" id="db"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  id="db"  autocomplete="off"><option  name="db" value="">请选择一个数据库</option>'
				var selectHtml = '';
				for (var i=0; i <response["data"].length; i++){
					if (response["data"][i]["count"] > 0){
						selectHtml += '<option selected="selected" name="db" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["db_env"] + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_name"] +  ' | ' + response["data"][i]["db_mark"] + '</option>' 
					}else{
						selectHtml += '<option name="db" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["db_env"] + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_name"] +  ' | ' + response["data"][i]["db_mark"] + '</option>' 
					}
					 
				};                        
				binlogHtml =  binlogHtml + selectHtml + '</select>';
				document.getElementById("db").innerHTML= binlogHtml;							
				$('.selectpicker').selectpicker('refresh');							
			}					
		});	
	})
	
	$(function() {
	    if ($("#databaseSQLExecuteHistroy").length) {  	
		    var columns = [
	    		            { "data": "id" },
	    		            { "data": "db_env"},
	    		            { "data": "db_host","className": "text-center" },
	    		            { "data": "db_name","className": "text-center"},
	    		            { "data": "exe_user","className": "text-center"},
	    		            { "data": "exe_sql"},	    		            
	    		            { "data": "exec_status","defaultContent": ''},
	    		            { "data": "exe_time","defaultContent": ''},
	    		            { "data": "exe_result","defaultContent": ''},
	    		            { "data": "create_time"},   
			        ]
		   var columnDefs = [  
		    		        	{
	    	   	    				targets: [1],
	    	   	    				render: function(data, type, row, meta) {
	    	   	                        if(row.db_env=="测试环境"){
	    	   	                        	return '<span class="label label-success">测试</span>'
	    	   	                        }else{
	    	   	                        	return '<span class="label label-danger">生产</span>'
	    	   	                        }
	    	   	    				},
	    	   	    				"className": "text-center",
	    		    		     },    
		    		        	{
	    	   	    				targets: [6],
	    	   	    				render: function(data, type, row, meta) {
	    	   	                        if(row.exec_status==0){
	    	   	                        	return '<span class="label label-success">成功</span>'
	    	   	                        }else{
	    	   	                        	return '<span class="label label-danger">失败</span>'
	    	   	                        }
	    	   	    				},
	    	   	    				"className": "text-center",
	    		    		     },	    		    		      		    		        
	    		                 {
    								targets: [5],
    								render: function(data, type, row, meta) {  
    									if (row.exe_sql.length > 100){
    										return '<button type="button" name="btn-sql-detail" data-toggle="modal" class="btn btn-link" value="'+ row.id +'">'+row.exe_sql.substring(-1,10)+'...</button>'
    									}
    									else{
    										return '<button type="button" name="btn-sql--detail" data-toggle="modal" class="btn btn-link" value="'+ row.id +'">'+row.exe_sql+'</button>'
    									}
    					              
    								},
	    					     }, 
			    		      ]	
		    var buttons = [{
		        text: '<span class="fa fa-plus"></span>',
		        className: "btn-xs",
		        action: function ( e, dt, node, config ) {
		        	return false
		        }	        
		    }]
		    InitSQLHistroyDataTable("databaseSQLExecuteHistroy","/api/logs/sql/",buttons,columns,columnDefs)  
		    sqlHistroyDataList
			if(sqlHistroyDataList["results"].length){
				for (var i = 0; i < sqlHistroyDataList["results"].length; ++i) {
					sqlHistroyResults[sqlHistroyDataList["results"][i]["id"]] = sqlHistroyDataList["results"][i]["exe_sql"]
				}
			}		    
	    }
	})
	
	$(function() {
		$("#db").change(function(){
			   var obj = document.getElementById("db"); 
			   var index = obj.selectedIndex;
			   var value = obj.options[index].value; 
			   RefreshSQLHistroyDataTable('databaseSQLExecuteHistroy','/api/logs/sql/?exe_db='+value)
		});			
	})
	
	$(function(){
	    $("button[name^='page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshSQLHistroyDataTable('databaseSQLExecuteHistroy', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	})
    
	$(function(){
	    $('#databaseSQLExecuteHistroy tbody').on('click', 'button[name="btn-sql-detail"]', function () {
	    	var id = $(this).val()
	        $(this).pt({
	            position: 'b', // 默认属性值
	            align: 'c',	   // 默认属性值
	            height: 'auto',
	            width: 'auto',
	            content: "<pre>"+sqlHistroyResults[id]+"</pre>"
	        });         
	    });  		
	})
	
})