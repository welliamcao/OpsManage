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
	for (var i=0; i <response.length; i++){
		if(response[i]["count"]==1){
			sList.push({"id":response[i]["name"],"name":response[i]["name"]})
		}
		else{
			aList.push({"id":response[i]["name"],"name":response[i]["name"]})
		}
	}					
	return {"group":sList,"all":aList}
}

function InitServerDatabaseDataTable(tableId,url,buttons,columns,columnDefs){
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

function RefreshServerDatabaseTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
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

function InitUserDatabaseDataTable(tableId,dataList,buttons,columns,columnDefs){
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
		    		"autoWidth": true	    			
		    	});
}

function RefreshUserDatabaseTable(tableId, urlData){
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

function BusinessAssetsSelect(node,ids){
	   if ( node > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/business/nodes/assets/'+ node + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="db_assets_id" id="db_assets_id" required><option  name="db_assets_id" value="">请选择服务器</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						if(ids==response[i]["id"]){
							selectHtml += '<option selected=selected name="db_assets_id" value="'+ response[i]["id"] +'">' + response[i]["detail"]["ip"] + '</option>'
						}else{
							selectHtml += '<option name="db_assets_id" value="'+ response[i]["id"] +'">' + response[i]["detail"]["ip"] + '</option>'
						}
						
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#db_assets_id").html(binlogHtml)
					$('.selectpicker').selectpicker('refresh');						
				},
			});	
	   }	
}

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);
}

function oBtBusinessSelect(){
	   $('#db_host').empty();
	   var obj = document.getElementById("db_business"); 
	   var index = obj.selectedIndex;
	   var businessId = obj.options[index].value; 
	   if ( businessId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/business/nodes/assets/'+ businessId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="db_assets_id" id="db_assets_id" required><option  name="db_assets_id" value="">请选择服务器</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						 selectHtml += '<option name="db_assets_id" value="'+ response[i]["id"] +'">' + response[i]["detail"]["ip"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#db_assets_id").html(binlogHtml)
					$('.selectpicker').selectpicker('refresh');						
				},
			});	
	   }
	   else{
		   $('#db_service').attr("disabled",true);
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
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="db_server" id="db_server"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"   autocomplete="off"><option  name="db_server" value="">请选择一个数据库</option>'
	var selectHtml = '';
	for (var i=0; i <response["data"].length; i++){
		selectHtml += '<option name="db_server" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["db_env"] + ' | '  + response["data"][i]["db_mark"] + ' | ' + response["data"][i]["ip"] +  ' | ' + response["data"][i]["db_port"] + ' | ' + response["data"][i]["db_rw"]  +  '</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= binlogHtml;							
	$('#'+ids).selectpicker('refresh');			
}	

function makeServerDatabaseTableList(vIds){
    var columns = [
                   {"data": "db_name"},
                   {
                	   "data": "db_size",
                	   "defaultContent": ""
                   },                  
	               ]
   var columnDefs = [     		        
	    		        {
   	    				targets: [2],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	    	                               	                           
	    	                           '<button type="button" name="btn-server-database-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
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

        }
    }]    
    InitServerDatabaseDataTable('server_database_list',"/api/db/server/"+vIds+"/list/",buttons,columns,columnDefs);	
}	

$(document).ready(function() {	
	
	$(function() {
		if($('#user').length){
			$.ajax({
				async : true,  
				url:'/api/user/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="user" id="user"  autocomplete="off"><option selected="selected" value="">请选择一个用户</option>	'
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
		if($('#db_business').length){
			$.ajax({
				async : true,  
				url:'/api/business/last/', //请求地址
				type:"GET",  //提交类似
				success:function(response){		
					var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="db_business"  id="db_business" autocomplete="off" onchange="javascript:ipvsVipBusinessSelect();"><option selected="selected" value="">请选择一个进行操作</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						selectHtml += '<option value="'+ response[i]["id"] +'">'+ response[i]["paths"] +'</option>' 					 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#db_business").html(binlogHtml)							
					$("#db_business").selectpicker('refresh');					
				}					
			});			
		}	 		
	})		
	
/*	$(function() {
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
	})*/	
	
	
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
    	makeDatabaseSelect("db_server",response)
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
    		            { "data": "db_business_paths" },
    		            { "data": "db_type"},
    		            { "data": "db_version"},
    		            { "data": "ip"},
    		            { "data": "db_user"},
    		            { "data": "db_port"},
    		            { "data": "db_mark"},
    		            { "data": "db_rw"},     
		        ]
	   var columnDefs = [     		    		        
		    		        {
	   	    				targets: [12],
	   	    				render: function(data, type, row, meta) {
	   	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-database-link" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="glyphicon glyphicon glyphicon-zoom-in" aria-hidden="true"></span>' +	
		    	                           '</button>' +	
		    	                           '<button type="button" name="btn-database-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +  
		    	                           '<button type="button" name="btn-database-import" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"  data-toggle="modal" data-target=".bs-example-modal-database-import"><span class="fa fa-database" aria-hidden="true"></span>' +	
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
    	function makeUserDatabaseTableList(dataList){
    	    var columns = [
    		               {"data": "username"},
    		               {
    		            	   "data": "db_name",
    		            	   "defaultContent": ""
    		               },
    		               {"data": "ip"},
    		               {"data": "db_port"},
    		               {"data": "db_mark"},
    		               {"data": "db_rw"},
    		               ]
    	   var columnDefs = [     		    		        
    		    		        {
    	   	    				targets: [6],
    	   	    				render: function(data, type, row, meta) {
    	   	                        return '<div class="btn-group  btn-group-xs">' +	
    		    	                           '<button type="button" name="btn-userdb-table" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-user-table"><span class="fa fa-ban" aria-hidden="true"></span>' +	
    		    	                           '</button>' +    		    	                           	                				                            		                            			                          			                            
    		    	                           '</div>';
    	   	    				},
    	   	    				"className": "text-center",
    		    		        },
    		    		      ]	
    	    var buttons = []
    	    InitUserDatabaseDataTable('user_database_list',dataList,buttons,columns,columnDefs);	
    	}	
     //makeUserDatabaseTableList('/db/config/?type=get_user_db')
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
					"db_version":$("#db_version").val(),
					"db_business":$("#db_business option:selected").val(),
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
					"db_version":$("#db_version").val(),
					"db_business":$("#db_business option:selected").val(),
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
            	BusinessAssetsSelect(response["db_business"],response["db_assets_id"])
            	DynamicSelect("db_env",response["db_env"])   	
            	DynamicSelect("db_business",response["db_business"])	
            	DynamicSelect("db_mode",response["db_mode"])
            	DynamicSelect("db_rw",response["db_rw"])	          												
				$("#db_version").val(response["db_version"]);	
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
    	var port = td.eq(9).text()
    	var server = td.eq(7).text()
		$.confirm({
		    title: '删除确认',
		    content:  '<strong>服务器</strong><code>' + server + ':' + port + '</code>数据库配置',
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

    $('#DatabaseListTable tbody').on('click',"button[name='btn-database-import']",function(){   
	  	var vIds = $(this).val(); 
	  	var td = $(this).parent().parent().parent().find("td")
    	let server = td.eq(7).text()
    	let port = td.eq(9).text()
    	$("#databaseImportModalLabel").html('<h4 class="modal-title" id="databaseImportModalLabel"><u class="red">'+ server + ':' + port +'</u> 导入数据库</h4>')
    	$("#server_database_submit").val(vIds)
		if ($('#server_database_list').hasClass('dataTable')) {
	        dttable = $('#server_database_list').dataTable();
	        dttable.fnClearTable();
	        dttable.fnDestroy();         
		}	    	
	  	makeServerDatabaseTableList(vIds)
	  });    
    	

    $('#server_database_list tbody').on('click',"button[name='btn-server-database-delete']",function(){   
	  	var vIds = $(this).val(); 
	  	var td = $(this).parent().parent().parent().find("td")
	  	let db_server = $("#server_database_submit").val()
		$.confirm({
		    title: '删除确认',
		    content:  '<strong>数据库</strong><code>' + td.eq(0).text() + '</code>',
		    type: 'red',
		    buttons: {
		             删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:'/api/db/server/'+ db_server +'/db/'+ vIds +'/' ,    
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
		        		if ($('#server_database_list').hasClass('dataTable')) {
		        	        dttable = $('#server_database_list').dataTable();
		        	        dttable.fnClearTable();
		        	        dttable.fnDestroy();         
		        		}	    	
		        	  	makeServerDatabaseTableList(db_server)  
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});		  	
	  });
    
    
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
	$('#user_database_list tbody').on('click',"button[name='btn-userdb-table']",function(){
	  	var vIds = $(this).val(); 
	  	let uid = $('#user :selected').val() 
	  	let colname = $(this).parent().parent().parent().find("td") 
	  	let dbname = colname.eq(1).text()
	  	let username =  colname.eq(0).text()
    	$("#userTableListSubmit").val(vIds)
    	$("#myUserTablesModalLabel").html('<h4 class="modal-title">用户<code>'+ username +'</code>分配<code>'+ dbname +'</code>数据库表</h4>')
    	$('select[name="user-table-list"]').empty();
    	var data = GetTableListOfDatabase('/api/db/user/'+ uid  +'/db/'+vIds+'/table/')
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
	
//	$('#user_database_list tbody').on('click',"button[name='btn-userdb-grants']",function(){
//	  	var vIds = $(this).val(); 
//	  	let colname = 	 $(this).parent().parent().parent().find("td")
//	  	var uid = colname.eq(1).find("span").attr("title") 
//	  	var dbname = colname.eq(3).text()
//	  	var username =  colname.eq(1).text()
//    	$("#userGrantsListSubmit").val(vIds)
//    	$("#myUserGrantsModalLabel").html('<h4 class="modal-title">用户<code>'+ username +'</code>分配<code>'+ dbname +'</code>数据库权限</h4>')
//    	$('select[name="user-grants-list"]').empty();
//    	var data = GetTableListOfDatabase('/db/users/?type=get_user_db_grants&&id=' + vIds)
//		$('select[name="user-grants-list"]').doublebox({
//	        nonSelectedListLabel: '选择权限',
//	        selectedListLabel: '已分配权限',
//	        preserveSelectionOnMove: 'moved',
//	        moveOnSelect: false,
//	        nonSelectedList:data["all"],
//	        selectedList:data["group"],
//	        optionValue:"id",
//	        optionText:"name",
//	        doubleMove:true,
//	      });	
//    });		
	
    $("#userTableListSubmit").on('click', function() {
    	var vIds = $(this).val();
    	let uid = $('#user :selected').val()
    	var formData = new FormData();
    	let tbList = new Array;
		$('select[name="user-table-list"] option:selected').each(function(){
			tbList.push($(this).val())
			formData.append("table_name",$(this).val())
        });	    	    	
    	$.ajax({  
            type: "POST",             
            url:"/api/db/user/"+ uid +"/db/"+ vIds +"/table/",
			processData: false,
			contentType: false,		            
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
            }  
    	}); 
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
	  
    $("#server_database_submit").on('click', function() {
    	var vIds = $(this).val();
		let dbname = $("#server_database_input").val()
		let url = "/api/db/server/"+vIds+"/list/"
    	if (vIds.length && dbname.length){
	    	$.ajax({  
	            type: "POST",             
	            url:url,  
	            data:{
	            	"db_name":dbname,
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
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
	            	RefreshServerDatabaseTable('#server_database_list', url) 
	            }  
	    	}); 
    	}else{
	    	$.confirm({
	    		title: '<strong>警告</strong>',
	    		typeAnimated: true,
	    	    content: "没有选择数据库服务器，或者没有输入数据库名称~",
	    	    type: 'red'		    	    
	    	});		    		
    	}
	
    });	
    
    $("#user").change(function(){ 
		let uid = $('#user :selected').val()   
		if(uid.length){
			$("#db_server_db").empty();
			let dataList = requests('get',"/api/db/user/list/")
			if ($('#user_database_list').hasClass('dataTable')) {
		        dttable = $('#user_database_list').dataTable();
		        dttable.fnClearTable();
		        dttable.fnDestroy();         
			}	 	
			let user_db_list = new Array();
			$(dataList).each(function(i){
				if(dataList[i]["count"] > 0){
					user_db_list.push(dataList[i])
				}
				   
			});			
			makeUserDatabaseTableList(user_db_list)
		}
    })    
    
    $("#db_server").change(function(){ 
		let sid = $('#db_server :selected').val()
		let uid = $('#user :selected').val()   
		if(sid.length && uid.length){
			$("#db_server_db").empty();
			let dataList = requests('get',"/api/db/user/"+uid+"/server/"+sid+"/list/")
			if ($('#user_database_list').hasClass('dataTable')) {
		        dttable = $('#user_database_list').dataTable();
		        dttable.fnClearTable();
		        dttable.fnDestroy();         
			}	 	
			let user_db_list = new Array();
			$(dataList).each(function(i){
				if(dataList[i]["count"] > 0){
					user_db_list.push(dataList[i])
				}
				   
			});			
			makeUserDatabaseTableList(user_db_list)
			var binlogHtml = '<select multiple required="required" class="selectpicker form-control" data-live-search="true" name="db_server_db" id="db_server_db"  data-size="10" data-selected-text-format="count > 4"  data-width="100%"   autocomplete="off">'
			var selectHtml = '';
			for (var i=0; i <dataList.length; i++){
				if(dataList[i]["count"] > 0){
					selectHtml += '<option name="db_server_db" value="'+ dataList[i]["id"] +'" selected="selected">' + dataList[i]["db_name"] + '</option>'
				}else{
					selectHtml += '<option name="db_server_db" value="'+ dataList[i]["id"] +'">' + dataList[i]["db_name"] + '</option>' 	 
				}
				
			};                        
			binlogHtml =  binlogHtml + selectHtml + '</select>';
			document.getElementById("db_server_db").innerHTML= binlogHtml;							
			$('.selectpicker').selectpicker('refresh');
			$("#add_user_db_btn").attr("disabled",false)
		}
    })
    
    $("#add_user_db_btn").on('click', function() {
    	var formData = new FormData();
		let sid = $('#db_server :selected').val()
		let uid = $('#user :selected').val() 
		let dbList = new Array();
		$("#db_server_db option:selected").each(function(){
			formData.append("dbIds",$(this).val())
        });	
		if(sid.length && uid.length){
			$.ajax({
				url:"/api/db/user/"+uid+"/server/"+sid+"/list/", //请求地址
				processData: false,
				contentType: false,				
				type:"POST",  //提交类似			
				data:formData,  //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: "保存成功",
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });	
	    			if ($('#user_database_list').hasClass('dataTable')) {
	    		        dttable = $('#user_database_list').dataTable();
	    		        dttable.fnClearTable();
	    		        dttable.fnDestroy();         
	    			}	 	
	    			let user_db_list = new Array();
	    			$(response).each(function(i){
	    				if(response[i]["count"] > 0){
	    					user_db_list.push(response[i])
	    				}
	    				   
	    			});	
	    			makeUserDatabaseTableList(user_db_list)
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
})