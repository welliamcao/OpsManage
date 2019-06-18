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

function GetTableListOfDatabase(url,){
	var aList = []
	var sList = []
	response = requests('get',url)
	if(response["code"]=="200"){
		for (var i=0; i <response["data"].length; i++){
			if(response["data"][i]["count"]==1){
				sList.push({"id":response["data"][i]["name"],"name":response["data"][i]["name"]})
			}
			else{
				aList.push({"id":response["data"][i]["name"],"name":response["data"][i]["name"]})
			}
		}			
		
	}
	return {"group":sList,"all":aList}
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
		    		"data":	data["data"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": true	    			
		    	});
}

function RefreshTable(tableId, urlData){
  $.getJSON(urlData, null, function( dataList )
  {
    table = $(tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList["data"].length; i++)
    {
      table.oApi._fnAddData(oSettings, dataList["data"][i]);
    }

    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
      
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

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

function ServicetSelect(projectId,serviceId){
	   if ( projectId > 0){	 
	   		var response = requests('get','/api/project/'+ projectId + '/',{})
			var binlogHtml = '<select class="selectpicker" name="deploy_service" id="db_service" required><option selected="selected" name="db_service" value="">请选择业务类型</option>'
			var selectHtml = '';
			for (var i=0; i <response["service_assets"].length; i++){
				 selectHtml += '<option name="db_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
			};                        
			binlogHtml =  binlogHtml + selectHtml + '</select>';
			return binlogHtml			
		} 
}


function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);
}

function oBtProjectSelect(){
	   $('#db_service').removeAttr("disabled");
	   $('#db_host').empty();
	   var obj = document.getElementById("db_project"); 
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/project/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="deploy_service" id="db_service" required><option selected="selected" name="db_service" value="">请选择业务类型</option>'
					var selectHtml = '';
					for (var i=0; i <response["service_assets"].length; i++){
						 selectHtml += '<option name="db_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					document.getElementById("db_service").innerHTML= binlogHtml;	
					$('#db_service').selectpicker('refresh');	
						
				},
			});	
	   }
	   else{
		   $('#db_service').attr("disabled",true);
	   }
}

function AssetsTypeSelect(model,ids){
	   var obj = document.getElementById(ids); 
	   var index = obj.selectedIndex;
	   var sId = obj.options[index].value; 
	   if ( sId  > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/assets/server/query/', //请求地址
				type:"POST",  //提交类似
				async:false,
				data:{
					"query":model,
					"id":sId
				},
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="db_assets_id" id="db_assets_id" required><option  name="db_assets_id" value="">请选择服务器</option>'
					var selectHtml = '';
					for (var i=0; i <response["data"].length; i++){
						 selectHtml += '<option name="db_assets_id" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					document.getElementById("db_assets_id").innerHTML= binlogHtml;	
					$('.selectpicker').selectpicker('refresh');			
				},
			});	
	   }
}


function format ( data ) {
    /* base */
    var trBaseHtml = '';
	for (var i=0; i <data['base'].length; i++){	
		if (i%6 == 0){
			trBaseHtml += '</tr>';
		}
		if (data['base'][i]["value"] == 'ON'){
			trBaseHtml += '<td>'+ data['base'][i]["name"] +':</td>'+ '<td><font color="green">'+ data['base'][i]["value"] +'</font></td>'		
		}
		else if (data['base'][i]["value"] == 'OFF'){
			trBaseHtml += '<td>'+ data['base'][i]["name"] +':</td>'+ '<td><font color="red">'+ data['base'][i]["value"] +'</font></td>'		
		}
		else{
			trBaseHtml += '<td>'+ data['base'][i]["name"] +':</td>'+ '<td>'+ data['base'][i]["value"] +'</td>'			
		}
			        
	};
    var vBaseHtml = '<div class="row"><div class="col-lg-12"><table class="table table-bordered"><caption>基本信息</caption>'+ 
							'<tr>' + trBaseHtml  + '</tr>' +
					'</table></div></div>';	
	/*  pxc */				
	var trPxcHtml = '';
	for (var i=0; i <data['pxc'].length; i++){	
		if (data['pxc'][i]["value"] == 'ON'){
			trPxcHtml += '<tr><td>'+ data['pxc'][i]["name"] +':</td>'+ '<td><font color="green">'+ data['pxc'][i]["value"] +'</font></td></tr>'
		}
		else if (data['pxc'][i]["value"] == 'OFF'){
			trPxcHtml += '<tr><td>'+ data['pxc'][i]["name"] +':</td>'+ '<td><font color="red">'+ data['pxc'][i]["value"] +'</font></td></tr>'
		}
		else{
			trPxcHtml += '<tr><td>'+ data['pxc'][i]["name"] +':</td>'+ '<td>'+ data['pxc'][i]["value"] +'</td></tr>'
		}
		
	};	
 	var vPXCHmtl = '<div class="col-lg-6"><table class="table table-bordered"><caption>PXC集群信息</caption>'+ 
							trPxcHtml  +
					'</table></div>'; 
	/* master */
	var trMasterHtml = '';
	for (var i=0; i <data['master'].length; i++){	
		trMasterHtml += '<tr><td>'+ data['master'][i]["name"] +':</td>'+ '<td>'+ data['master'][i]["value"] +'</td></tr>'
	}
    var vMasterHtml = '<div class="col-lg-4"><table class="table table-bordered"><caption>Master信息</caption>'+ 
							'<tr>' + trMasterHtml  +'</tr>'
					  '</table></div>';	
	/* slave */
	var trSlaveHtml = '';
	for (var i=0; i <data['slave'].length; i++){	
		if (i%4 == 0){
			trSlaveHtml += '</tr>';
		}	
		if (data['slave'][i]["value"] == 'Yes'){
			trSlaveHtml += '<td>'+ data['slave'][i]["name"] +':</td>'+ '<td><font color="green">'+ data['slave'][i]["value"] +'</font></td>'
		}
		else if (data['slave'][i]["value"] == 'No'){
			trSlaveHtml += '<td>'+ data['slave'][i]["name"] +':</td>'+ '<td><font color="red">'+ data['slave'][i]["value"] +'</font></td>'
		}
		else{
			trSlaveHtml += '<td>'+ data['slave'][i]["name"] +':</td>'+ '<td>'+ data['slave'][i]["value"] +'</td>'
		}
		
	}
    var vSlaveHtml = '<div class="row"><div class="col-lg-12"><table class="table table-bordered"><caption>Slave信息</caption>'+ 
							'<tr>' + trSlaveHtml  +'</tr>'
					  '</table></div></div>';	
	/* 汇总 */				  
	if (data['pxc'].length > 0 && data['master'].length > 5){
		return vBaseHtml + '<div class="row">'  + vPXCHmtl  + vMasterHtml + '</div>';
	} 
	else if (data['slave'].length > 0){
		return vBaseHtml  + vSlaveHtml + '</div>';
	}
	else if( data['pxc'].length > 0 ){
		return vBaseHtml + '<div class="row">' + vPXCHmtl + '</div>';
	}
	else if ( data['slave'].length > 0 &&  data['master'].length > 5){
		return vBaseHtml + vSlaveHtml + vMasterHtml + '</div>';
	}
	else if(data['master'].length > 5){
		return vBaseHtml + '<div class="row">' + vMasterHtml + '</div>';
	}
	else{
		return vBaseHtml
	}
}

function makeDatabaseSelect(ids,response){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="db" id="db"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  id="db"  autocomplete="off"><option  name="db" value="">请选择一个数据库</option>'
	var selectHtml = '';
	for (var i=0; i <response["data"].length; i++){
		if(response["data"][i]["db_env"]=="beta"){
			var db_env = "测试环境"
		}else{
			var db_env = "生产环境"
		}
		selectHtml += '<option name="db" value="'+ response["data"][i]["id"] +'">' + db_env + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_name"] + ' | ' + response["data"][i]["db_rw"]  +  ' | ' + response["data"][i]["db_mark"] + '</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= binlogHtml;							
	$('#'+ids).selectpicker('refresh');			
}	
	

$(document).ready(function() {	
	
	$(function() {
		if($('#user').length){
			$.ajax({
				async : true,  
				url:'/api/user/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="user" id="user"  autocomplete="off"><option selected="selected" value="">请选择一个用户</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						selectHtml += '<option value="'+ response[i]["id"] +'">'+ response[i]["username"] +'</option>' 					 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					document.getElementById("user").innerHTML= binlogHtml;							
					$('#user').selectpicker('refresh');							
				}					
			});				
		}
	})	

	$(function() {
		if($('#db_project').length){
			$.ajax({
				async : true,  
				url:'/api/project/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="db_project"  id="db_project" autocomplete="off" onchange="javascript:oBtProjectSelect();"><option selected="selected" value="">请选择一个项目</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						selectHtml += '<option value="'+ response[i]["id"] +'">'+ response[i]["project_name"] +'</option>' 					 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					document.getElementById("db_project").innerHTML= binlogHtml;							
					$('#db_project').selectpicker('refresh');							
				}					
			});			
		}	 		
	})		
	
	$(function() {
		if($('#query_db').length ){
			$.ajax({
				async : true,  
				url:'/db/manage/?type=query_user_db', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					makeDatabaseSelect("query_db",response);
					makeDatabaseSelect("table_schema",response);	
					makeDatabaseSelect("binlog_db",response);
					makeDatabaseSelect("optimize_db",response);
				}					
			});				
		}
	})	
	
	
	try
		{
			if($("#db_query_btn").length){
		    	var aceEditAdd = setAceEditMode("compile-editor-add","ace/mode/mysql","ace/theme/sqlserver");							
			}
 		  
		}
	catch(err)
		{
			console.log(err)
		}
	

	
    if ($("#DatabaseListTable").length) {
    	var response = requests('get','/db/config/?type=get_all_db',{})
    	makeDatabaseSelect("db",response)
	    var columns = [
    	   	            {
    		                "className":      'details-control',
    		                "orderable":      false,
    		                "data":           null,
    		                "defaultContent": ''
    		            },
    		            { "data": "id" },
    		            { "data": "db_env" },
    		            { "data": "db_mode" },
    		            { "data": "project" },
    		            { "data": "service"},
    		            { "data": "db_type"},
    		            { "data": "db_name"},
    		            { "data": "ip"},
    		            { "data": "db_user"},
    		            { "data": "db_port"},
    		            { "data": "db_mark"},
    		            { "data": "db_rw"},     
		        ]
	   var columnDefs = [  
	    		        	{
    	   	    				targets: [2],
    	   	    				render: function(data, type, row, meta) {
    	   	                        if(row.db_env=="beta"){
    	   	                        	return '<span class="label label-success">测试</span>'
    	   	                        }else{
    	   	                        	return '<span class="label label-danger">生产</span>'
    	   	                        }
    	   	    				},
    	   	    				"className": "text-center",
    		    		        },     		    		        
		    		        {
	   	    				targets: [13],
	   	    				render: function(data, type, row, meta) {
	   	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-database-link" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="glyphicon glyphicon glyphicon-zoom-in" aria-hidden="true"></span>' +	
		    	                           '</button>' +	
		    	                           '<button type="button" name="btn-database-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +    		    	                           
		    	                           '<button type="button" name="btn-database-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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
	    	  	$("#save_database_config").val("");	
	    	  	$("#save_database_config").text("添加");
	        }	        
	    }]
	    var table = $('#DatabaseListTable').DataTable({
				    "dom": "Bfrtip",
				    "buttons":buttons,				  
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	response["data"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": true	    			
		});        
	    $('#DatabaseListTable tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );
	        dbId = row.data()["id"];
	        $.ajax({
	            url : "/api/db/status/"+dbId+"/",
	            type : "post",
	            async : false,
	            data : {"id":dbId},
	            dataType : "json",
	            success : function(result) {
	            	dataList = result.data;
	            }
	        });	         
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( format(dataList) ).show();
	            tr.addClass('shown');
	        }
	    });	    
    }
    
    if ($("#customSQLList").length) {
    	function makeCustomSqlTableList(){
    	    var columns = [
    	                   {"data": "id","className": "text-center"},
    		               {"data": "sql","className": "text-center"},
    		               ]
    	   var columnDefs = [    		    		        
    		    		        {
    	   	    				targets: [2],
    	   	    				render: function(data, type, row, meta) {
    	   	                        return '<div class="btn-group  btn-group-xs">' +	
    		    	                           '<button type="button" name="btn-sql-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
    		    	                           '</button>' +		                				                            		                            			                          
    		    	                           '<button type="button" name="btn-sql-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
    		    	                           '</button>' +			                            
    		    	                           '</div>';
    	   	    				},
    	   	    				"className": "text-center",
    		    		        },
    		    		      ]	
    	    var buttons = [{
    	        text: '<span class="fa fa-plus"></span>',
    	        className: "btn-xs",
    	    }]
    		InitDataTable('customSQLList','/db/config/?type=get_custom_sql',buttons,columns,columnDefs);	
    	}	
    	makeCustomSqlTableList()  	    
    }      
    
    if ($("#user_database_list").length) {
    	function makeUserDatabaseTableList(){
    	    var columns = [
    	                   {"data": "id"},
    		               {"data": "username"},
    		               {"data": "db_env"},
    		               {"data": "db_name"},
    		               {"data": "ip"},
    		               {"data": "db_port"},
    		               {"data": "db_mark"},
    		               {"data": "db_rw"},
    		               ]
    	   var columnDefs = [
 		    		        	{
    	   	    				targets: [1],
    	   	    				render: function(data, type, row, meta) {
    	   	                        return '<span title="'+row.uid+'">'+ row.username +'</span>';
    	   	    				},
    	   	    				"className": "text-center",
    		    		        },   
 		    		        	{
        	   	    				targets: [2],
        	   	    				render: function(data, type, row, meta) {
        	   	                        if(row.db_env=="beta"){
        	   	                        	return '<span class="label label-success">测试</span>'
        	   	                        }else{
        	   	                        	return '<span class="label label-danger">生产</span>'
        	   	                        }
        	   	    				},
        	   	    				"className": "text-center",
        		    		        },     		    		        
    		    		        {
    	   	    				targets: [8],
    	   	    				render: function(data, type, row, meta) {
    	   	                        return '<div class="btn-group  btn-group-xs">' +	
    		    	                           '<button type="button" name="btn-userdb-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-info"><span class="fa fa-edit" aria-hidden="true"></span>' +	
    		    	                           '</button>' +	
    		    	                           '<button type="button" name="btn-userdb-table" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-user-table"><span class="fa fa-ban" aria-hidden="true"></span>' +	
    		    	                           '</button>' +    		    	                           	                				                            		                            			                          
    		    	                           '<button type="button" name="btn-userdb-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
    		    	                           '</button>' +			                            
    		    	                           '</div>';
    	   	    				},
    	   	    				"className": "text-center",
    		    		        },
    		    		      ]	
    	    var buttons = []
    		InitDataTable('user_database_list','/db/config/?type=get_user_db',buttons,columns,columnDefs);	
    	}	
     makeUserDatabaseTableList()
    }  

	$('#save_database_config').on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);
		var vIds = $(this).val();
		var form = document.getElementById('addDatabase');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;
			if (value.length == 0 && name.length >0 ){
				$("[name='"+ name +"']").parent().addClass("has-error");
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 	
                btnObj.removeAttr('disabled');			
				return false;
			}else if (value.length > 0){
				$("[name='"+ name +"']").parent().removeClass("has-error");
			}
			
		};	
		if (vIds > 0){
			$.ajax({
				url:'/api/db/config/'+ vIds +'/', //请求地址
				type:"PUT",  //提交类似
				contentType : "application/json",
				data:JSON.stringify({
					"db_env":$("#db_env option:selected").val(),
					"db_type":$("#db_type").val(),
					"db_name":$("#db_name").val(),
					"db_assets_id":$("#db_assets_id option:selected").val(),
					"db_user":$("#db_user").val(),
					"db_passwd":$("#db_passwd").val(),
					"db_port":$("#db_port").val(),
					"db_mark":$("#db_mark").val(),
					"db_rw":$("#db_rw").val(),
					"db_mode":$("#db_mode option:selected").val(),
				}),
				success:function(response){
					btnObj.removeAttr('disabled');
					RefreshTable('#DatabaseListTable', '/db/config/?type=get_all_db') 	                				
					
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
			})			
		}else{
			$.ajax({
				url:'/api/db/config/', //请求地址
				type:"POST",  //提交类似
				contentType : "application/json", 
				data:JSON.stringify({
					"db_env":$("#db_env option:selected").val(),
					"db_type":$("#db_type").val(),
					"db_name":$("#db_name").val(),
					"db_assets_id":$("#db_assets_id option:selected").val(),
					"db_user":$("#db_user").val(),
					"db_passwd":$("#db_passwd").val(),
					"db_port":$("#db_port").val(),
					"db_mark":$("#db_mark").val(),
					"db_rw":$("#db_rw").val(),
					"db_mode":$("#db_mode option:selected").val(),
				}),
				success:function(response){
					btnObj.removeAttr('disabled');
					RefreshTable('#DatabaseListTable', '/db/config/?type=get_all_db') 	                				
					
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
			})			
		}
    	
	}); 
	
	$('#DatabaseListTable tbody').on('click',"button[name='btn-database-link']",function(){   
    	var vIds = $(this).val();
		$.ajax({
			dataType: "JSON",
			url:'/api/db/org/'+ vIds +'/', //请求地址
			type:"POST",  //提交类似
			success:function(response){
				$('#chart-container').html("");
	    	    $('#chart-container').orgchart({
	      	      'data' : response.data,
	      	      'nodeContent': 'title',
	      	      'direction': 'l2r', 
	      	      'exportFilename': 'MySQL',
	      	      'exportButton': false,
	      	    }); 				
			}					
		});	 	
    });	
	//new
    $('#DatabaseListTable tbody').on('click',"button[name='btn-database-edit']",function(){  
		var btnObj = $(this);
		btnObj.attr('disabled',true);		  
	  	var vIds = $(this).val(); 
	  	$("#save_database_config").val(vIds);	
	  	$("#save_database_config").text("修改");
        $.ajax({  
            url : '/api/db/config/'+ vIds + '/' ,  
            type : 'get', 
            async:false,
            success : function(response){
            	btnObj.removeAttr('disabled');
            	DynamicSelect("db_env",response["db_env"])   	
            	DynamicSelect("db_project",response["db_project"])	
            	DynamicSelect("db_mode",response["db_mode"])
            	DynamicSelect("db_rw",response["db_rw"])	
				$("#db_service").html(ServicetSelect(response["db_project"],response["db_service"]));
				DynamicSelect("db_service",response["db_service"])
				AssetsTypeSelect('service','db_service');		
				DynamicSelect("db_assets_id",response["db_assets_id"])											
				$("#db_name").val(response["db_name"]);	
				$("#db_type").val(response["db_type"]);	
				$("#db_user").val(response["db_user"]);	
				$("#db_port").val(response["db_port"]);	
				$("#db_mark").val(response["db_mark"]);	
				$('.selectpicker').selectpicker('refresh');					  
            },
            error:function(response){
	    		btnObj.removeAttr('disabled');
	    	}	            
        });		
	  });	
    $('#DatabaseListTable tbody').on('click',"button[name='btn-database-delete']",function(){   
	  	var vIds = $(this).val(); 
	  	var td = $(this).parent().parent().parent().find("td")
    	var text = td.eq(6).text()
    	var server = td.eq(7).text()
		$.confirm({
		    title: '删除确认',
		    content:  '<strong>服务器</strong><code>' + server + '</code>数据库【<strong>' + text +'</strong>】配置',
		    type: 'red',
		    buttons: {
		             删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:'/api/db/config/'+ vIds + '/' ,    
		            error: function(response) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });     
		            },  
		            success: function(response) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshTable('#DatabaseListTable', '/db/config/?type=get_all_db')   
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});			
	  });
	  
    $("#add_inception_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);    
		$.ajax({
/* 				dataType: "JSON", */
			url:'/api/inc/config/', //请求地址
			type:"POST",  //提交类似			
			data:$("#add_inception").serializeObject(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
	            window.location.reload();	                								
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
	//new
    $("#save_custom_btn").on('click', function() {
		var btnObj = $(this);
		var vIds = $(this).val();
		btnObj.attr('disabled',true);  
		if (vIds > 0){
			$.ajax({
				url:'/api/sql/custom/'+ vIds +'/', //请求地址
				type:"PUT",  //提交类似			
				data:$("#add_custom_sql").serializeObject(),  //提交参数
				success:function(response){
					btnObj.removeAttr('disabled');
					RefreshTable('#customSQLList', '/db/config/?type=get_custom_sql') 	               								
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
		}else{
			$.ajax({
				url:'/api/sql/custom/', //请求地址
				type:"POST",  //提交类似			
				data:$("#add_custom_sql").serializeObject(),  //提交参数
				success:function(response){
					btnObj.removeAttr('disabled');
					RefreshTable('#customSQLList', '/db/config/?type=get_custom_sql')              								
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
		}  		 	
    });	
    //new
    $('#customSQLList tbody').on('click',"button[name='btn-sql-edit']",function(){ 
    	var vIds = $(this).val();
    	$("#save_custom_btn").val(vIds)
		$.ajax({
			dataType: "JSON",
			url:'/api/sql/custom/'+ vIds +'/', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				$("#sql").val(response["sql"]);	
				RefreshTable('#customSQLList', '/db/config/?type=get_custom_sql') 
			}					
		});	 	
    });	 
    //new
    $('#customSQLList tbody').on('click',"button[name='btn-sql-delete']",function(){  
	  	var vIds = $(this).val(); 		  	
    	var text = $(this).parent().parent().parent().find("td").eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content: text,
		    type: 'red',
		    buttons: {
		             删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:'/api/sql/custom/'+ vIds + '/' ,    
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
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshTable('#customSQLList', '/db/config/?type=get_custom_sql') 
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});			
	  });  
	 //new
    $("#add_user_db_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);    
		$.ajax({
/* 				dataType: "JSON", */
			url:'/db/users/', //请求地址
			type:"POST",  //提交类似			
			data:$("#add_user_db").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				if(response["code"]==500){
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response["msg"],
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 					
				}else{
	            	new PNotify({
	                    title: 'Success!',
	                    text: "添加成功",
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });		
	            	RefreshTable('#user_database_list', '/db/config/?type=get_user_db')  
				}
                								
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
    
    //new
    $('#user_database_list tbody').on('click',"button[name='btn-userdb-edit']",function(){  
	  	var vIds = $(this).val(); 	
	  	var uid = $(this).parent().parent().parent().find("td").eq(1).find("span").attr("title") 	
	  	$("#add_user_db_btn").hide();
   		$("#modf_user_db_btn").show();	
   		$("#modf_user_db_btn").val(vIds);    	
		$.ajax({
			dataType: "JSON",
			url:'/db/users/?type=get_all_user_db&uid='+ uid, //请求地址
			type:"GET",  //提交类似
			success:function(response){
				console.log(response)	
				DynamicSelect("user",uid)
				var binlogHtml = '<select multiple required="required" class="selectpicker form-control" data-live-search="true" name="db" id="db"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  id="db"  autocomplete="off"><option  name="db" value="">请选择一个数据库</option>'
				var selectHtml = '';
				for (var i=0; i <response["data"].length; i++){
					if (response["data"][i]["count"] > 0){
						selectHtml += '<option selected="selected" name="db" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["db_env"] + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_name"]+ ' | ' + response["data"][i]["db_rw"]  +  ' | ' + response["data"][i]["db_mark"] + '</option>' 
					}else{
						selectHtml += '<option name="db" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["db_env"] + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_name"] + ' | ' + response["data"][i]["db_rw"]  +  ' | ' + response["data"][i]["db_mark"] + '</option>' 
					}
					 
				};                        
				binlogHtml =  binlogHtml + selectHtml + '</select>';
				document.getElementById("db").innerHTML= binlogHtml;							
				$('.selectpicker').selectpicker('refresh');							
			}					
		});			
	  });  
	  
	$('#user_database_list tbody').on('click',"button[name='btn-userdb-table']",function(){
	  	var vIds = $(this).val(); 
	  	let colname = 	 $(this).parent().parent().parent().find("td")
	  	var uid = colname.eq(1).find("span").attr("title") 
	  	var dbname = colname.eq(3).text()
	  	var username =  colname.eq(1).text()
    	$("#userTableListSubmit").val(vIds)
    	$("#myUserTablesModalLabel").html('<h4 class="modal-title">用户<code>'+ username +'</code>分配<code>'+ dbname +'</code>数据库表</h4>')
    	$('select[name="user-table-list"]').empty();
    	var data = GetTableListOfDatabase('/db/users/?type=get_user_db_tables&&id=' + vIds)
		$('select[name="user-table-list"]').doublebox({
	        nonSelectedListLabel: '选择表',
	        selectedListLabel: '已分配表',
	        preserveSelectionOnMove: 'moved',
	        moveOnSelect: false,
	        nonSelectedList:data["all"],
	        selectedList:data["group"],
	        optionValue:"id",
	        optionText:"name",
	        doubleMove:true,
	      });	
    });		  
	
	$('#user_database_list tbody').on('click',"button[name='btn-userdb-grants']",function(){
	  	var vIds = $(this).val(); 
	  	let colname = 	 $(this).parent().parent().parent().find("td")
	  	var uid = colname.eq(1).find("span").attr("title") 
	  	var dbname = colname.eq(3).text()
	  	var username =  colname.eq(1).text()
    	$("#userGrantsListSubmit").val(vIds)
    	$("#myUserGrantsModalLabel").html('<h4 class="modal-title">用户<code>'+ username +'</code>分配<code>'+ dbname +'</code>数据库权限</h4>')
    	$('select[name="user-grants-list"]').empty();
    	var data = GetTableListOfDatabase('/db/users/?type=get_user_db_grants&&id=' + vIds)
		$('select[name="user-grants-list"]').doublebox({
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
	
    $("#userTableListSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="user-table-list"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/db/users/",  
	            data:{
	            	"type":"modf_user_tables",
					"id": vIds,
					"table_name":vServer
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

    $("#userGrantsListSubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="user-grants-list"]').val()
    	if (vServer){
	    	$.ajax({  
	            type: "POST",             
	            url:"/db/users/",  
	            data:{
	            	"type":"modf_user_grants",
					"id": vIds,
					"grants":vServer
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
	  
    $("#modf_user_db_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);  
		var dbList = [];
        $("#db option:selected").each(function () {
            dbList.push($(this).val())
        });			
		$.ajax({
/* 				dataType: "JSON", */
			url:'/db/users/', //请求地址
			type:"PUT",  //提交类似			
			data:{
				"user":$("#user option:selected").val(),
				"db":dbList
			},  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				if(response["code"]==500){
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response["msg"],
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 					
				}else{
	            	new PNotify({
	                    title: 'Success!',
	                    text: "修改成功",
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });		
	            	RefreshTable('#user_database_list', '/db/config/?type=get_user_db')  
				}                  								
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	           	new PNotify({
	                   title: 'Ops Failed!',
	                   text: response["msg"],
	                   type: 'error',
	                   styling: 'bootstrap3'
	            }); 
	    	}
		});			 	
    });	
    
    $('#user_database_list tbody').on('click',"button[name='btn-userdb-delete']",function(){ 
		var vIds = $(this).val();  
		var userInfo = $(this).parent().parent().parent().find("td")	
		var user = userInfo.eq(1).text();
		var uid = userInfo.find("span").attr("title");
		var db_name = $(this).parent().parent().parent().find("td").eq(3).text(); 
		$.confirm({
		    title: '删除确认',
		    content:   '<strong>'+user+'</strong>' + "对<code>" + db_name +"</code>的操作权限",
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:'/db/users/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
						"uid":uid
					}, 
					success:function(response){
						if(response["code"]==500){
				           	new PNotify({
				                   title: 'Ops Failed!',
				                   text: response["msg"],
				                   type: 'error',
				                   styling: 'bootstrap3'
				            }); 					
						}else{
			            	new PNotify({
			                    title: 'Success!',
			                    text: "删除成功",
			                    type: 'success',
			                    styling: 'bootstrap3'
			                });		
			            	RefreshTable('#user_database_list', '/db/config/?type=get_user_db')  
						}              								
					},
			    	error:function(response){
			           	new PNotify({
			                   title: 'Ops Failed!',
			                   text: response["msg"],
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
    	     	   
    $("#db_query_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true); 
		$('#show_sql_result').show();	
		var db = $('#query_db option:selected').val() 	
		var sql = aceEditAdd.getSession().getValue();
	    if ( sql.length == 0 || db == 0){
        	new PNotify({
                title: 'Warning!',
                text: 'SQL内容与数据库不能为空',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
	    	btnObj.removeAttr('disabled');
	    	return false;
	    };		   
		$.ajax({
			url:'/db/manage/', 
			type:"POST",  			
			data:{
				"db":db,
				"model":'exec_sql',
				"sql":sql
			},  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				var ulTags = '<ul class="list-unstyled timeline widget">'	
				var tableHtml = ''
				var liTags = '';
				var tablesList = [];
				if (response['code'] == "200" && response["data"].length > 0 && response["data"][0]["dataList"][2].length > 0){
					for (var i=0; i <response["data"].length; i++){
						var tableId = "query_result_list_"+ i
						tablesList.push(tableId)
						if (response["data"][i]["dataList"][0] >= 0){
							var tableHtml = '<table class="table" id="'+ tableId +'"><thead><tr>'
							var trHtml = '';
							for (var x=0; x <response["data"][i]["dataList"][2].length; x++){
								trHtml = trHtml + '<th>' + response["data"][i]["dataList"][2][x] +'</th>';
							}; 	
							tableHtml = tableHtml + trHtml + '</tr></thead><tbody>';
							var trsHtml = '';
							for (var y=0; y <response["data"][i]["dataList"][1].length; y++){
								var tdHtml = '<tr>';
								for (var z=0; z < response["data"][i]["dataList"][1][y].length; z++){
									tdHtml = tdHtml + '<td>' + response["data"][i]["dataList"][1][y][z] +'</td>';
								} 	
								trsHtml = trsHtml + tdHtml + '</tr>';
							}                    	
							tableHtml = tableHtml + trsHtml +  '</tbody></table>';														
						}else{
							tableHtml = response["data"][i]["dataList"]

						}
						liTags = liTags + '<li>' +
							                '<div class="block">' +
							                  '<div class="block_content">' +
							                    '<h2 class="title">' +
							                       '<span >耗时：'+ response["data"][i]["time"] +'</span>' +
							                    '</h2><br>' + tableHtml +
							                  '<br><br></div>' +
							                '</div>' +
							              '</li>'				
						}
					$("#result").html(ulTags + liTags + '</ul>');
				    if (tablesList.length) {
				    	for (var i=0; i <tablesList.length; i++){
						   var table = $("#"+tablesList[i]).DataTable( {
						        dom: 'Bfrtip',
						        buttons: [{
					                    extend: "copy",
					                    className: "btn-sm"
					                },
					                {
					                    extend: "csv",
					                    className: "btn-sm"
					                },
					                {
					                    extend: "excel",
					                    className: "btn-sm"
					                },
					                {
					                    extend: "pdfHtml5",
					                    className: "btn-sm"
					                },
					                {
				                    extend: "print",
					                    className: "btn-sm"
					            }],
								language : {
									"sProcessing" : "处理中...",
									"sLengthMenu" : "显示 _MENU_ 项结果",
									"sZeroRecords" : "没有匹配结果",
									"sInfo" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
									"sInfoEmpty" : "显示第 0 至 0 项结果，共 0 项",
									"sInfoFiltered" : "(由 _MAX_ 项结果过滤)",
									"sInfoPostFix" : "",
									"sSearch" : "搜索:",
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
							},					            
						   });	
						}				    		
				    }						
				}
				else if (response['code'] == "200" && response["data"].length > 0 && response["data"][0]["dataList"][2].length == 0){
					var selectHtml = '<div id="result"><pre>执行成功，耗时：'+ response["data"][0]["time"] +'，影响行数：' + response["data"][0]["dataList"][0] + '</pre></div>';
					$("#result").html(selectHtml);						
				}	
				else {
					var selectHtml = '<div id="result"><pre>执行失败，' + response["msg"] + '</pre></div>';
					$("#result").html(selectHtml);						
				}	                								
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
	if ($("#binlog_time").length){
		var cdate = new Date();
		var startTime =  getFormatDate(0)
		var endTime = getFormatDate(3600)
		$("#binlog_time").val(endTime+' - '+startTime)
	 	$("#binlog_time").daterangepicker({
            "timePicker": true,
            "timePicker24Hour": true,
            "linkedCalendars": false,
            "autoUpdateInput": false,
            "locale": {
                format: "YYYY-MM-DD hh:mm:ss",
                applyLabel: "应用",
                cancelLabel: "取消",
                resetLabel: "重置",
            }
	    });	
	}

    
	$("#binlog_db").change(function(){
		var obj = document.getElementById("binlog_db"); 
	    var index = obj.selectedIndex;
		var value = obj.options[index].value; 
		$.ajax({
			url:'/db/manage/', //请求地址
			type:"POST",  //提交类似			
			data:{
				"db":value,
				"model":"binlog_sql",
			},  //提交参数
			success:function(response){
	            //window.location.reload();	
	            if (response["code"] == 200){
		            if (response["data"].length) {
						var selectHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="binlog_db_file" id="binlog_db_file"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  autocomplete="off"><option>请选择一个binlog文件</option>' 
						var option = '';
						for (var i=0; i <response["data"].length; i++){
							option = option + '<option value="'+ response["data"][i] +'">'+ response["data"][i] +'</option>'
						}													
						var selectHtml = selectHtml + option + '</select>';
						$("#binlog_db_file").html(selectHtml);
						$('.selectpicker').selectpicker('refresh');	
					}		            
	            }else{
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response["msg"],
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 	            	
	            }                            								
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
	});    
    
    $("#db_binlog_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);    
		$.ajax({
			url:'/db/manage/',
			type:"POST",			
			data:$("#parse_binlog_file").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');    
				var binlogHtml = '<div id="binlog_result"><pre><code class="sql hljs">';
				for (var i=0; i <response["data"].length; i++){
					binlogHtml +=  response["data"][i]+'<br>';
				}; 		
				binlogHtml = binlogHtml + '</code></pre></div>';
				$("#binlog_result").html(binlogHtml);  
			    $('pre code').each(function(i, block) {
			    	hljs.highlightBlock(block);
			  	});				
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	           	new PNotify({
	                   title: 'Ops Failed!',
	                   text: response["msg"],
	                   type: 'error',
	                   styling: 'bootstrap3'
	           	}); 
	    	}
		});	    
    });	   
    
	$("#table_schema").change(function(){
		var obj = document.getElementById("table_schema"); 
	    var index = obj.selectedIndex;
		var value = obj.options[index].value; 
		$.ajax({
			url:'/db/manage/', //请求地址
			type:"POST",  //提交类似			
			data:{
				"db":value,
				"model":"table_list",
			},  //提交参数
			success:function(response){ 
	            if (response["data"].length) {
					var selectHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="table_name" id="table_name"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  autocomplete="off">' 
					var option = '';
					for (var i=0; i <response["data"].length; i++){
						option = option + '<option value="'+ response["data"][i] +'">'+ response["data"][i] +'</option>'
					}													
					var selectHtml = selectHtml + option + '</select>';
					$("#table_name").html(selectHtml);
					$('.selectpicker').selectpicker('refresh');	
				}	                           								
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
	});     
    
    $("#db_schema_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);    
		$.ajax({
			url:'/db/manage/',
			type:"POST",			
			data:$("#table_schema_form").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');
				var schemaTableHtml = '<table class="table table-striped">' +		                
							              '<tbody>' +
							                '<tr>' +
							                  '<td>数据库: </td>' + '<td>'+ response["data"]["schema"][1][0][0] +'</td>' +
							                  '<td>表名: </td>' +	'<td>'+ response["data"]["schema"][1][0][1] +'</td>' +
							                  '<td>表类型: </td>' + '<td>'+ response["data"]["schema"][1][0][2] +'</td>' +	
							                '</tr>' +
							                '<tr>' +  
							                  '<td>存储引擎: </td>' + '<td>'+ response["data"]["schema"][1][0][3] +'</td>' +	
							                  '<td>版本: </td>' + '<td>'+ response["data"]["schema"][1][0][4] +'</td>' +						
							                  '<td>行格式: </td>' + '<td>'+ response["data"]["schema"][1][0][5] +'</td>' +		
							                '</tr>' +  
							                '<tr>' +  
							                  '<td>行记录数: </td>' + '<td>'+ response["data"]["schema"][1][0][6] +'</td>' +	
							                  '<td>数据长度: </td>' + '<td>'+ response["data"]["schema"][1][0][7] +'</td>' +		
							                  '<td>最大数据长度: </td>' + '<td>'+ response["data"]["schema"][1][0][8] +'</td>' +	
								            '</tr>' +	
								            '<tr>' + 
							                  '<td>索引长度: </td>' + '<td>'+ response["data"]["schema"][1][0][9] +'</td>' +	
							                  '<td>数据空闲: </td>' + '<td>'+ response["data"]["schema"][1][0][10] +'</td>' +	
							                  '<td>自动递增值: </td>' + '<td>'+ response["data"]["schema"][1][0][11] +'</td>' +	
									        '</tr>' +	
									        '<tr>' + 							                  
							                  '<td>创建日期: </td>' + '<td>'+ response["data"]["schema"][1][0][12] +'</td>' +	
							                  '<td>字符集类型: </td>' + '<td>'+ response["data"]["schema"][1][0][13] +'</td>' +	
							                  '<td>注释</td>' + '<td>'+ response["data"]["schema"][1][0][14] +'</td>' +	
							                '</tr>'	 +                       
							              '</tbody>' +
							           '</table>'                    					
				var indexTableHtml = '<table class="table table-striped"><thead><tr>'     	
				    var indexTrHtml = '';
					for (var i=0; i <response["data"]["index"][2].length; i++){
						indexTrHtml = indexTrHtml + '<th>' + response["data"]["index"][2][i] +'</th>';
					}; 
					indexTableHtml = indexTableHtml + indexTrHtml + '</tr></thead><tbody>';
					var indexHtml = '';
					for (var i=0; i <response["data"]["index"][1].length; i++){
						var indexTdHtml = '<tr>';
						for (var x=0; x < response["data"]["index"][1][i].length; x++){
							indexTdHtml = indexTdHtml + '<td>' + response["data"]["index"][1][i][x] +'</td>';
						} 	
						indexHtml = indexHtml + indexTdHtml + '</tr>';
					}                    	
				indexTableHtml = indexTableHtml + indexHtml +  '</tbody></table>';						
				var descHtml = '<pre><code class="sql hljs">' + response["data"]["desc"] + '<br></code></pre>';	
                var schemaHtml = '<div id="schema_result"><ul class="list-unstyled timeline widget">' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>表结构信息</a>' +
					                    '</h2><br>' +
					                    schemaTableHtml +
					                  '</div>' +
					                '</div>' +
					              '</li>' +
					              '<li>' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>表索引信息</a>' +
					                    '</h2><br>' +
					                    indexTableHtml +
					                  '</div>' +					                  
					                '</div>' +
					              '</li>' +
					               '<li>' +
					                '<div class="block">' +
					                  '<div class="block_content">' +
					                    '<h2 class="title">' +
					                       '<a>DDL信息</a>' +
					                    '</h2><br>' +					                    
					                    descHtml +
					                  '</div>' +
					                '</div>' +
					              '</li>' +					              
					            '</ul>'				
				$("#schema_result").html(schemaHtml);   
			    $('pre code').each(function(i, block) {
			    	hljs.highlightBlock(block);
			  	});				
				           								
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
    
    $("#db_optimize_btn").on('click', function() {
		var btnObj = $(this);
		btnObj.attr('disabled',true);    
		$.ajax({
			url:'/db/manage/',
			type:"POST",			
			data:$("#optimize_sql").serialize(),  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');    
	            if (response["code"] == 200){
		            if (response["data"].length) {
						$("#optimize_result").html("<pre>"+ response['data'][0] +"</pre>"); 
					}		            
	            }else{
		           	new PNotify({
		                   title: 'Ops Failed!',
		                   text: response["msg"],
		                   type: 'error',
		                   styling: 'bootstrap3'
		            }); 	            	
	            }  				
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