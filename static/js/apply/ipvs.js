var webssh = false
function make_terminal(term,element,ws_url,data) { 
    if (webssh) {
        return;
    }        
    webssh = true;        	
    term.open(element);

    term.write('正在连接...')
             
    var ws = new WebSocket(ws_url);
    ws.onopen = function (event) {
        term.resize(term.cols, term.rows);

        ws.send(data); 

        ws.onmessage = function (event) {
        	term.write(event.data);
        };      
    };
    ws.onerror = function (e) {
    	term.write('\r\n连接失败')
    	ws = false
    };
   
    return {socket: ws, term: term};
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

function makeMultipleVipSelect(ids,name,dataList){
	var binlogHtml = '<select multiple required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" id='+ ids +' name="'+ name +'"autocomplete="off">'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		var text = dataList[i]["vip"] + ':' + dataList[i]["port"] + ' | ' + dataList[i]["project"]+' | '+dataList[i]["line"]+' | '+dataList[i]["desc"]					
		selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>'				 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("#"+ids).html(binlogHtml)
	$("#"+ids).selectpicker('refresh');	
}

function ipvsVipProjectSelect(){
	   $("#ipvs_vip_service").removeAttr("disabled");
	   $("#ipvs_assets").empty();
	   var obj = document.getElementById("ipvs_vip_project"); 
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/project/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="ipvs_vip_service" id="ipvs_vip_service" required><option selected="selected" value="">请选择业务类型</option>'
					var selectHtml = '';
					for (var i=0; i <response["service_assets"].length; i++){
						 selectHtml += '<option name="ipvs_vip_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#ipvs_vip_service").html(binlogHtml)
					$(".selectpicker").selectpicker('refresh');	
						
				},
			});	
	   }
	   else{
		   $("select[name='ipvs_vip_service']").attr("disabled",true);
	   }
}

function IpvsVipAssetsTypeSelect(model,ids){
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
					var binlogHtml = '<select class="selectpicker" name="ipvs_assets" id="ipvs_assets" required><option  name="ipvs_assets" value="">请选择服务器</option>'
					var selectHtml = '';
					for (var i=0; i <response["data"].length; i++){
						 selectHtml += '<option name="ipvs_assets" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#ipvs_assets").html(binlogHtml)
					$('.selectpicker').selectpicker('refresh');			
				},
			});	
	   }
}

function ipvsRealServerProjectSelect(){
	   $("#ipvs_rs_service").removeAttr("disabled");
	   $("#rs_assets").empty();
	   var obj = document.getElementById("ipvs_rs_project"); 
	   var index = obj.selectedIndex;
	   var projectId = obj.options[index].value; 
	   if ( projectId > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/api/project/'+ projectId + '/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select class="selectpicker" name="ipvs_rs_service" id="ipvs_rs_service" required><option selected="selected" value="">请选择业务类型</option>'
					var selectHtml = '';
					for (var i=0; i <response["service_assets"].length; i++){
						 selectHtml += '<option name="ipvs_rs_service" value="'+ response["service_assets"][i]["id"] +'">' + response["service_assets"][i]["service_name"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#ipvs_rs_service").html(binlogHtml)
					$(".selectpicker").selectpicker('refresh');	
						
				},
			});	
	   }
	   else{
		   $("select[name='ipvs_vip_service']").attr("disabled",true);
	   }
}

function IpvsRealServerAssetsTypeSelect(model,ids){
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
					var binlogHtml = '<select class="selectpicker" name="rs_assets" id="rs_assets" required><option  name="rs_assets" value="">请选择服务器</option>'
					var selectHtml = '';
					for (var i=0; i <response["data"].length; i++){
						 selectHtml += '<option name="rs_assets" value="'+ response["data"][i]["id"] +'">' + response["data"][i]["ip"] + '</option>' 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#rs_assets").html(binlogHtml)
					$('.selectpicker').selectpicker('refresh');			
				},
			});	
	   }
}

function makeDynamicSelect(dataList,selectName,selectValue){
	var makeSelect = '<select class="form-control" name="'+selectName+'">'
	var selectOption = ''
	for (var i = 0; i < dataList.length; ++i) {
		if(dataList[i]==selectValue){
			selectOption += '<option value="'+ dataList[i] +'" selected="selected">'+ dataList[i] +'</option>'
		}else{
			selectOption += '<option value="'+ dataList[i] +'" >'+ dataList[i] +'</option>'
		}        				 
	}		
	return makeSelect = makeSelect + selectOption + '</select>'    	
}

var forword_type = { 
    '-m':'NAT',
    '-g':'DR',
    '-i':'TUN',
    '-b':'FULLNAT'		
}

var protocol_type = { 
	    '-t':'TCP',
	    '-u':'UDP',	
}

var scheduler_mode = {
	'sh':'地址哈希',
	'rr':'轮训',
	'wrr':'加权轮询',        
	'lc':'最少连接',        
	'wlc':'加权最少链接'	
}

var ipvs_vip_table_type = {
	"key":"all",
	"id":0
}

var ipvs_rs_table_type = {

}

function checkValue(value){
	if(value){
		return value
	}
	else{
		return ""
	}
}
	
function AssetsSelect(name,dataList,selectIds){
	
	if(!selectIds){selectIds=0}
	
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:ipvsVipProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		var text = dataList[i]["ip"]+ ' | ' + dataList[i]["project"]+' | '+dataList[i]["service"]				
		if(selectIds==dataList[i]["id"]){
			selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
		}else{
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		} 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}


function IpvsVipSelect(name,dataList,selectIds){
	
	if(!selectIds){selectIds=0}
	
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:ipvsVipProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个VIP进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		var text = dataList[i]["vip"]+ ':' + dataList[i]["port"] + ' | '  + dataList[i]["project"] + ' | ' + dataList[i]["line"] + ' | ' + dataList[i]["desc"]			
		if(selectIds==dataList[i]["id"]){
			selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
		}else{
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		} 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
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

function InitDataTable(tableId,dataList,buttons,columns,columnDefs){
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
		    		"iDisplayLength": 20,
		            "select": {
		                "style":    'multi',
		                "selector": 'td:first-child'
		            },		    		
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});

	    if (dataList['next']){
	    	  $("button[name='vip_page_next']").attr("disabled", false).val(dataList['next']);	
	      }else{
	    	  $("button[name='vip_page_next']").attr("disabled", true).val();
	      }
	      if (dataList['previous']){
	    	  $("button[name='vip_page_previous']").attr("disabled", false).val(dataList['previous']);	
	      }else{
	    	  $("button[name='vip_page_previous']").attr("disabled", true).val();
	      }	  
	  
		$('input[name="vip_is_active"]').bootstrapSwitch({  
	        onText:"上线",  
	        offText:"下线",  
	        onColor:"success",  
	        offColor:"danger",  
	        size:"mini",
	        onSwitchChange:function(event,state){  
	            if(state==true){  
	               console.log('已打开');  
	            }else{  
	            	console.log('已关闭');  
	            }  
	            console.log(this.value)
	            if(state==true){  
	                var data = {
	            			"id":this.value,
	            			"is_active":1
	            		} 
	            }else{  
	                var data = {
	            			"id":this.value,
	            			"is_active":0
	            		}  
	            }  
	            updateIpvsStatus('/apply/ipvs/vip/status/'+this.value+'/',data,'vip')
	        }  
	    }) 
	}

function RefreshVipTable(tableId, urlData){
	  $.getJSON(urlData, null, function( dataList )
	  {
	    table = $(tableId).dataTable();
	    oSettings = table.fnSettings();
	    
	    table.fnClearTable(this);

	    for (var i=0; i<dataList["results"].length; i++)
	    {
	      table.oApi._fnAddData(oSettings, dataList["results"][i]);
	    }

	    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
	    table.fnDraw();	
	    
	    if (dataList['next']){
	    	  $("button[name='vip_page_next']").attr("disabled", false).val(dataList['next']);	
	      }else{
	    	  $("button[name='vip_page_next']").attr("disabled", true).val();
	      }
	      if (dataList['previous']){
	    	  $("button[name='vip_page_previous']").attr("disabled", false).val(dataList['previous']);	
	      }else{
	    	  $("button[name='vip_page_previous']").attr("disabled", true).val();
	      }		    
	    
		$('input[name="vip_is_active"]').bootstrapSwitch({  
	        onText:"上线",  
	        offText:"下线",  
	        onColor:"success",  
	        offColor:"danger",  
	        size:"mini",
	        onSwitchChange:function(event,state){  
	            if(state==true){  
	               console.log('已打开');  
	            }else{  
	            	console.log('已关闭');  
	            }  
	            console.log(this.value)
	            if(state==true){  
	                var data = {
	            			"id":this.value,
	            			"is_active":1
	            		} 
	            }else{  
	                var data = {
	            			"id":this.value,
	            			"is_active":0
	            		}  
	            }  
	            updateIpvsStatus('/apply/ipvs/vip/status/'+this.value+'/',data,'vip')
	        }  
	    }) 	    
	    
	  });
	}

function AutoReload(tableId,url){
	  RefreshVipTable('#'+tableId, url);
	  setTimeout(function(){AutoReload(url);}, 30000);
}

	
function InitRealServerDataTable(tableId,url,buttons,columns,columnDefs){
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
		    		"iDisplayLength": 20,
		            "select": {
		                "style":    'multi',
		                "selector": 'td:first-child'
		            },			    		
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});
	  if (data['next']){
		  $("button[name='rs_page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='rs_page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='rs_page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='rs_page_previous']").attr("disabled", true).val();
	  }
	  
	$('input[name="rs_is_active"]').bootstrapSwitch({  
        onText:"上线",  
        offText:"下线",  
        onColor:"success",  
        offColor:"danger",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
               var data = {
            			"id":this.value,
            			"is_active":1
            		}
            }
            else{  
                var data = {
            			"id":this.value,
            			"is_active":0
                	}
            }    
            updateIpvsStatus('/apply/ipvs/rs/status/'+this.value+'/',data,'rs')
        }  
    }) 	  
	  
}

function InitNameServerDataTable(tableId,url,buttons,columns,columnDefs){
    if ($('#'+tableId).hasClass('dataTable')) {
        dttable = $('#'+tableId).dataTable();
        dttable.fnClearTable(); 
        dttable.fnDestroy(); 
      }	
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
		    		"iDisplayLength": 20,
		            "select": {
		                "style":    'multi',
		                "selector": 'td:first-child'
		            },			    		
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	    			
		    	});	 
	  if (data['next']){
		  $("button[name='ns_page_next']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='ns_page_next']").attr("disabled", true).val();
	  }
	  if (data['previous']){
		  $("button[name='ns_page_previous']").attr("disabled", false).val(data['next']);	
	  }else{
		  $("button[name='ns_page_previous']").attr("disabled", true).val();
	  }	  
}

function RefreshRealServerTable(tableId, urlData){
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
  	  $("button[name='rs_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='rs_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='rs_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='rs_page_previous']").attr("disabled", true).val();
    } 
    
	$('input[name="rs_is_active"]').bootstrapSwitch({  
        onText:"上线",  
        offText:"下线",  
        onColor:"success",  
        offColor:"danger",  
        size:"mini",
        onSwitchChange:function(event,state){  
            if(state==true){  
               var data = {
            			"id":this.value,
            			"is_active":1
            		}
            }
            else{  
                var data = {
            			"id":this.value,
            			"is_active":0
                	}
            }    
            updateIpvsStatus('/apply/ipvs/rs/status/'+this.value+'/',data,'rs')
        }  
    }) 	 
        
  });	
}

function RefreshNameServerTable(tableId, urlData){
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
  	  $("button[name='ns_page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='ns_page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='ns_page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='ns_page_previous']").attr("disabled", true).val();
    } 
          
  });	
}

function updateIpvsStatus(urls,data,ids){
	$.ajax({  
        type: "PUT",  
        url:urls, 
        dataType: "json",
		data:data,					
        error: function(response) {  
        	new PNotify({
                title: 'Ops Failed!',
                text: response.responseText,
                type: 'error',
                styling: 'bootstrap3'
            });       
        },  
        success: function(response) {  
			if (response["code"] == "200"){
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
        	if (ids=='vip'){
	            switch(ipvs_vip_table_type["key"]) {
	            case 'service':
	            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/tree/service/'+ ipvs_vip_table_type["id"] +'/')
	               	break;
	            case 'vip':
	            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/?id='+ ipvs_vip_table_type["id"])
	               	break;
	            default:
	            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')		
	            }         		
        	}else if(ids=='rs'){
        		RefreshRealServerTable('ipvsRSManageListTable', '/api/apply/ipvs/rs/?'+$.param(ipvs_rs_table_type))
        	}
        }  
	});	
}

	
function makeipvsVipManageTableList(dataList){
    var columns = [
		           {
		                "orderable": false,
		                "data":      null,
		                "className": 'select-checkbox', 
		                "defaultContent": ''
		            },                    
                   {"data": "vip"},
                   {"data": "sip"},     
                   {"data": "protocol"},
	               {"data": "scheduler"},
	               {"data": "rs_count"},
	               {"data": "persistence"},
	               {"data": "line"},
	               {"data": "desc"},
	               {"data": "is_active"},
	               ]
   var columnDefs = [                      
	    		        {
	   	    				targets: [1],
	   	    				render: function(data, type, row, meta) {  	    					
	   	                        return row.vip + ':' + row.port
	   	    				},	
	   	    				"className": "text-center",
		    		    },  	    		    
	    		        {
	   	    				targets: [3],
	   	    				render: function(data, type, row, meta) {  	    					
	   	                        return protocol_type[row.protocol]
	   	    				},
	   	    				"className": "text-center",
		    		    }, 		    		    
	    		        {
	   	    				targets: [9],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.is_active==1){
	   	    						return '<input class="switch switch-mini" name="vip_is_active" type="checkbox" data-size="mini"  value="'+ row.id + '" checked />'
	   	    					}else{
	   	    						return '<input class="switch switch-mini" name="vip_is_active" type="checkbox" data-size="mini"  value="'+ row.id + '"/>'
	   	    					}
	   	    				}
	    		        }, 		    		    
	    		        {
   	    				targets: [10],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-vip-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +  
	    	                           '<button type="button" name="btn-vip-add" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-plus" aria-hidden="true"></span>' +	
	    	                           '</button>' +	
	    	                           '<button type="button" name="btn-vip-rs" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-search" aria-hidden="true"></span>' +	
	    	                           '</button>' +	    	                           
	    	                           '<button type="button" name="btn-vip-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = [{
        text: '添加',
        className: "btn-sm",
        action: function ( e, dt, node, config ) {        	
        	$('#myAddIpvsVIPModal').modal("show")
        	}
    	},
        {
            text: '修改',
            className: "btn-sm",
            action: function (e, dt, button, config) {
            	//dt.rows().select();
            	let dataList = dt.rows('.selected').data()
            	var vips = ''
            	if (dataList.length==0){
            		$.alert({
            		    title: '操作失败',
            		    content: '批量修改VIP失败，请先选择VIP',
            		    type: 'red',		    
            		});	            		
            	}else{            		
    			    makeMultipleVipSelect('modf_ipvs_vip','ipvs_vip',dataList)
    			    $("#myModfIpvsVIPModal").modal("show")
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
	InitDataTable('ipvsVIPManageListTable',dataList,buttons,columns,columnDefs);	
}	



function makeipvsRealServerManageTableList(ids,url){
    var columns = [  
		           {
		                "orderable": false,
		                "data":      null,
		                "className": 'select-checkbox', 
		                "defaultContent": ''
		            },                   
                   {"data": "vip"},
                   {"data": "ipvs_fw_ip"},
                   {"data": "forword"},
                   {"data": "weight"},
                   {"data": "sip"},
                   {"data": "is_active"},
	               ]
   var columnDefs = [   
	    		        {
							targets: [1],
							render: function(data, type, row, meta) {  	    					
						       return '<span title="'+row.ipvs_vip+'">'+ row.vip_detail.vip + ":" + row.vip_detail.port +'</span>'
							},
							"className": "text-center",
						}, 	
	    		        {
							targets: [3],
							render: function(data, type, row, meta) {  	    					
						       return forword_type[row.forword]
							},
							"className": "text-center",
						},							
	    		        {
	   	    				targets: [6],
	   	    				render: function(data, type, row, meta) {
	   	    					if(row.is_active==1){
	   	    						return '<input class="switch switch-mini" name="rs_is_active" type="checkbox" data-size="mini"  value="'+ row.id + '" checked />'
	   	    					}else{
	   	    						return '<input class="switch switch-mini" name="rs_is_active" type="checkbox" data-size="mini"  value="'+ row.id + '"/>'
	   	    					}
	   	    				}
	    		        },						
	    		        {
   	    				targets: [7],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-realserver-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' + 	    	                           	    	                           
	    	                           '<button type="button" name="btn-realserver-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = [
                   {
                       text: '修改',
                       className: "btn-sm",
                       action: function (e, dt, button, config) {
                       	//dt.rows().select();
                    	console.log(ids)
                       	let dataList = dt.rows('.selected').data()
                       	if (dataList.length==0){
                       		$.alert({
                       		    title: '操作失败',
                       		    content: '批量修改RealServer失败，请先选择RealServer',
                       		    type: 'red',		    
                       		});	            		
                       	}else{
                       		let ipvs_vips = new Array()
                       		let rsSelectOption = ''
               			    for (var i=0; i< dataList.length; i++){
               			    	ipvs_vips.push(dataList[i]["ipvs_vip"])
               			    	rsSelectOption +=  '<option selected="selected" value="'+dataList[i]["id"]+'">' + dataList[i]["ipvs_fw_ip"] + '</option>'
               			    }                        		
               				var contentHtml = '<form role="form" data-parsley-validate class="form-horizontal form-label-left">' +
												'<fieldset>' +													
												'<div class="item form-group">'+
													 '<label class="col-sm-2 control-label">RS</label>'+
													 '<div class="col-sm-8">'+
					                                    '<select multiple="multiple" class="select2_multiple form-control" name="rs_ids" required>'+
					                                    	rsSelectOption +
					                                    '</select>' +
													 '</div>'+
												'</div>'+	
												'<div class="item form-group">'+
												  '<label class="col-sm-2 control-label">调度类型</label>'+
												  '<div class="col-sm-8">'+
												  '<select class="form-control" name="forword">'+
												     '<option value="-m">NAT</option><option value="-i">TUN</option><option selected="selected" value="-g">DR</option>'+
												  '</select>' +
												  '</div>'+
												 '</div>'+													
												'<div class="item form-group">'+
												 '<label class="col-sm-2 control-label">权重</label>'+
												 '<div class="col-sm-8">'+
												 	'<input type="text"  class="form-control" name="weight" placeholder="权重" value="" class="input-xlarge"></input>'+
												 '</div>'+
												 '</div>'+												
												'</fieldset>'+									 		
											   '</form>'				
						    $.confirm({
						        icon: 'fa fa-edit',
						        type: 'blue',
						        title: '修改RealServer权重',
						        content: contentHtml,
						        buttons: {
						            '取消': function() {},
						            '修改': {
						                btnClass: 'btn-blue',
						                action: function() {				
									    	$.ajax({  
									            type: "PUT",  
									            url:"/apply/ipvs/rs/batch/", 
									            dataType: "json",
												data: this.$content.find('form').serialize(),					
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
									            	var parameter={}
												    $("input[type='hidden']").each(function () {
												        var key = $(this).prop('name');
												        var value = $(this).val();
												        if (key != "csrfmiddlewaretoken"){
												        	parameter[key] = value;
												        	
												        }												        
												    })	
										        	switch(ids)
										        	{
										        	    case "ipvsRSManageListTable":
										        	    	RefreshRealServerTable(ids, '/api/apply/ipvs/rs/?'+$.param(parameter)) //下一页如何处理?
										        	        break;
										        	    case "ipvsVipRealServerManageListTable":
										        	    	RefreshRealServerTable(ids, '/api/apply/ipvs/rs/?ipvs_vip='+ipvs_vips[0])
										        	        break;
										        	}												    
													
									            }  
									    	});
						                }
						            }
						        }
						    });
               				
                       	}
                       }
                   },                   
                   {
                       text: '删除',
                       className: "btn-sm",
                       action: function (e, dt, button, config) {
                       	//dt.rows().select();
                       	let dataList = dt.rows('.selected').data()
                       	if (dataList.length==0){
                       		$.alert({
                       		    title: '操作失败',
                       		    content: '批量删除RealServer失败,请先选择RealServer',
                       		    type: 'red',		    
                       		});	            		
                       	}else{
                       		let ipvs_rs_id = new Array()
                       		let ipvs_rs_ip = new Array()
                       		let ipvs_vips = new Array()
               			    for (var i=0; i< dataList.length; i++){
               			    	ipvs_rs_id.push(dataList[i]["id"])
               			    	ipvs_vips.push(dataList[i]["ipvs_vip"])
               			    	ipvs_rs_ip.push(dataList[i]["ipvs_fw_ip"])
               			    } 
               				$.confirm({
               				    title: '删除确认',
               				    content: 'RealServer:<br> <strong>'+ipvs_rs_ip.join("<br>")+'</strong>',
               				    type: 'red',
               				    buttons: {
               				        删除: function () {		       
               						$.ajax({
               							url:"/apply/ipvs/rs/batch/", 
               							type:"DELETE",  		
               							data:{
               								"rs_ids":ipvs_rs_id,
               							}, 
               							success:function(response){
							            	var parameter={}
										    $("input[type='hidden']").each(function () {
										        var key = $(this).prop('name');
										        var value = $(this).val();
										        if (key != "csrfmiddlewaretoken"){
										        	parameter[key] = value;
										        	
										        }												        
										    })	
								        	switch(ids)
								        	{
								        	    case "ipvsRSManageListTable":
								        	    	RefreshRealServerTable(ids, '/api/apply/ipvs/rs/?'+$.param(parameter)) //下一页如何处理?
								        	        break;
								        	    case "ipvsVipRealServerManageListTable":
								        	    	RefreshRealServerTable(ids, '/api/apply/ipvs/rs/?ipvs_vip='+ipvs_vips[0])
								        	        break;
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
               				        },
               				        取消: function () {
               				            return true;			            
               				        },			        
               				    }
               				});               			    
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
    InitRealServerDataTable(ids,url,buttons,columns,columnDefs);	
}



function makeipvsNameServerManageTableList(ids,url){
    var columns = [  
		           {
		                "orderable": false,
		                "data":      null,
		                "className": 'select-checkbox', 
		                "defaultContent": ''
		            },                   
                   {"data": "vip"},
                   {"data": "nameserver"},
                   {"data": "desc"},
	               ]
   var columnDefs = [   										
	    		        {
   	    				targets: [4],
   	    				render: function(data, type, row, meta) {  	    					
   	                        return '<div class="btn-group  btn-group-xs">' +	
	    	                           '<button type="button" name="btn-nameserver-edit" value="'+ row.id +'" class="btn btn-default"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           '</button>' +    	                           	    	                           
	    	                           '<button type="button" name="btn-nameserver-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
	    	                           '</button>' +			                            
	    	                           '</div>';
   	    				},
   	    				"className": "text-center",
	    		        },
	    		      ]	
    var buttons = [                  
                   {
                       text: '删除',
                       className: "btn-sm",
                       action: function (e, dt, button, config) {
                       	//dt.rows().select();
                       	let dataList = dt.rows('.selected').data()
                       	if (dataList.length==0){
                       		$.alert({
                       		    title: '操作失败',
                       		    content: '批量删除NameServer失败,请先选择NameServer',
                       		    type: 'red',		    
                       		});	            		
                       	}else{
                       		let ipvs_ns_id = new Array()
                       		let ipvs_ns = new Array()
                       		let ipvs_vip = 0
               			    for (var i=0; i< dataList.length; i++){
               			    	ipvs_ns_id.push(dataList[i]["id"])
               			    	ipvs_ns.push(dataList[i]["nameserver"])
               			    	ipvs_vip = dataList[i]["ipvs_vip"]
               			    } 
               				$.confirm({
               				    title: '删除确认',
               				    content: 'NameServer:<br> <strong>'+ipvs_ns.join("<br>")+'</strong>',
               				    type: 'red',
               				    buttons: {
               				        删除: function () {		       
               						$.ajax({
               							url:"/apply/ipvs/ns/batch/", 
               							type:"DELETE",  		
               							data:{
               								"ns_ids":ipvs_ns_id,
               							}, 
               							success:function(response){
							            	new PNotify({
							                    title: 'Success!',
							                    text: '删除成功',
							                    type: 'success',
							                    styling: 'bootstrap3'
							                }); 
							            	RefreshRealServerTable('ipvsVipNameServerManageListTable', '/api/apply/ipvs/ns/?ipvs_vip='+ipvs_vip)
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
    InitNameServerDataTable(ids,url,buttons,columns,columnDefs);	
}

function search_go() {
    var parameter = {};
    $("input[type='hidden']").each(function () {
        var key = $(this).prop('name');
        var value = $(this).val();
        if (key != "csrfmiddlewaretoken"){
        	parameter[key] = value;
        	
        }
        
    })
    var count = 0;
    for (var i in parameter) {
        count += i;
        break;
    }
    ipvs_rs_table_type = parameter
    RefreshRealServerTable('ipvsRSManageListTable','/api/apply/ipvs/rs/?'+$.param(parameter))
}

function changepage(pageindex) {
    curpage = pageindex;
    search_go();
}

function removeself(obj) {
    $(obj).parent().remove();
    changepage(1);
}	

function viewIpvsNs(obj){
	var ids = obj["id"] - 30000
	makeipvsNameServerManageTableList('ipvsVipNameServerManageListTable','/api/apply/ipvs/ns/?ipvs_vip='+ids)
	$('#myModfIpvsNsModal').modal({show:true});
}

function viewRate(obj){
	var ids = obj["id"] - 30000
	$("#myModfVipStatusModalLabel").html('<p class="text-blank">IPVS VIP <code>'+obj["text"].split(" ")[0]+ '</code>Rate/速率</p>')
	$("#webssh_tt").html("")
	$('#vipsVipRealtimeStatus').val("rate|"+ids)
	$('#myModfIpvsVipStatusModal').modal({show:true});	
}

function viewStats(obj){
	var ids = obj["id"] - 30000   
	$("#myModfVipStatusModalLabel").html('<p class="text-blank">IPVS VIP <code>'+obj["text"].split(" ")[0]+ '</code>Stat/状态</p>')
	$("#webssh_tt").html("")
	$('#vipsVipRealtimeStatus').val("stats|"+ids)
	$('#myModfIpvsVipStatusModal').modal({show:true});
}

function customMenu(node) {
    var items = {
            "view":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "RealServer",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-search-plus",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewRealServer(obj)
					}
            },
            "config":{
          		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "域名管理",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-bookmark",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewIpvsNs(obj)
					}
          },              
            "rate":{
          		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "传输速率",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-bar-chart",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewRate(obj)				
					}
          }, 
          "stats":{
      		"separator_before"	: false,
				"separator_after"	: false,
				"_disabled"			: false, 
				"label"				: "连接状态",
				"shortcut_label"	: 'F2',
				"icon"				: "fa fa-terminal",
				"action"			: function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
					var parents = inst.get_path('#' + obj.parent ,false)
					var parentsName = ''
					for (var i=0; i <parents.length; i++){
						parentsName = parentsName + parents[i].split("(")[0]
					}
					viewStats(obj)				
				}
          },            
	  }
    if(node["id"]>10000 && node["id"] <= 20000){
  		try {    	  
	    	  delete items.view
	    	  delete items.rate
	    	  delete items.config
	    	  delete items.stats
  		}
  		catch(err) {
  			console.log(err)
  		}     	  
    }else if(node["id"]>30000){
	    	try {    	  
	    	  delete items.new
	    	  delete items.view	    	  
			}
			catch(err) {
				console.log(err)
			}     	  
    }else if(node["id"]>20000 && node["id"]<30000){
		try {
	      	  delete items.new
	    	  delete items.view
	    	  delete items.rate
	    	  delete items.config
	    	  delete items.stats
		}
		catch(err) {
			console.log(err)
		} 
    }
    return items
}

function viewRealServer(obj){
	$("#ipvs_vip_realserver_detail").show()
	let ids = obj["id"] - 30000
    if ($('#ipvsVipRealServerManageListTable').hasClass('dataTable')) {
        dttable = $('#ipvsVipRealServerManageListTable').dataTable();
        dttable.fnClearTable(); 
        dttable.fnDestroy(); 
    }	
	makeipvsRealServerManageTableList('ipvsVipRealServerManageListTable','/api/apply/ipvs/rs/?ipvs_vip='+ids)
}

function drawTree(ids,url){
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if ((op === "move_node" || op === "copy_node") && node.type && node.id > 10000  && node.id < 30000) {	    	    	
	    	        return false;
	    	    }
	    	    else if ((op === "move_node" || op === "copy_node") && node.type && node.id > 30000 && par.parent > 20000 && par.parent < 30000 ) {	
	    	    	return false;
	    	    	
	    	    }
	    	    return true;
	    	},
	      'data' : {
	        "url" : url,
	        "dataType" : "json" // needed only if you do not supply JSON headers
	      }
	    },	    
/*	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique","checkbox"],*/
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],
/*        "checkbox": {
            "keep_selected_style": false,//是否默认选中
            "three_state": false,//父子级别级联选择
            "tie_selection": false
        },*/	    
	    "contextmenu":{
		    	select_node:false,
		    	show_at_node:true,
		    	'items': customMenu
		      }	    
	});		
}

function makeIPVSVipTableListForJstree(url,position,parent,ids){
	$.ajax({  
        cache: true,  
        type: "GET",  
        url:url, 
        async : false,  
        error: function(response) {
        	new PNotify({
                title: 'Ops Failed!',
                text: response.responseText,
                type: 'error',
                styling: 'bootstrap3'
            });       
        },  
        success: function(response) {
        	if(ids=="service"){
    			for (var i=0; i <response["results"].length; i++){
    				if (response["results"][i]["is_active"]==1){
    					var icon = "fa fa-check-circle assets-online"
    				}else{
    					var icon = "fa fa-check-circle-o assets-offline"
    				}
    				var text = response["results"][i]["vip"]+':'+ response["results"][i]["port"]+' ('+ response["results"][i]["rs_count"] +')'
                    var newNode = {
                            "id": response["results"][i]["id"]+30000,
                            "text": text,
                            "icon": icon
                        }        						
    				$('#ipvsTree').jstree('create_node', parent, newNode, position, false, false);	
    			}
    			$("#ipvsTree").jstree("open_node", parent);       		
        	}
	        if ($('#ipvsVIPManageListTable').hasClass('dataTable')) {
	            dttable = $('#ipvsVIPManageListTable').dataTable();
	            dttable.fnClearTable(); //清空table
	            dttable.fnDestroy(); //还原初始化datatable
	        }
	        if ($('#ipvsVipRealServerManageListTable').hasClass('dataTable')) {
	            dttable = $('#ipvsVipRealServerManageListTable').dataTable();
	            dttable.fnClearTable();
	            dttable.fnDestroy();
	        }	
            $("#ipvs_vip_realserver_detail").hide()
            $("#add_ipvs_rs_task").hide()
            $("#ipvs_ns").hide()	        
			makeipvsVipManageTableList(response["results"])
        } 
	}); 	
}

$(document).ready(function() {	
	
	var randromChat = makeRandomId()
	
	drawTree('#ipvsTree',"/api/apply/ipvs/tree/")
	
    $("#ipvsTree").click(function () {
        var position = 'last';
        var parent = $("#ipvsTree").jstree("get_selected");
        if (parent[0] > 20000 && parent[0] < 30000){
        	$("#projectTree").jstree("open_node", parent[0]);
            let serviceId = parent[0]-20000
            ipvs_vip_table_type["key"] = 'service'
            ipvs_vip_table_type["id"] = serviceId	            
            makeIPVSVipTableListForJstree("/api/apply/ipvs/tree/service/" + serviceId + "/",position,parent,'service') 
            $("#modfIpvsVipsubmit").val("service|"+serviceId)
        }else if(parent[0] > 30000){
        	let vip_id = parent[0]-30000
            ipvs_vip_table_type["key"] = 'vip'
            ipvs_vip_table_type["id"] = vip_id         	  	
        	makeIPVSVipTableListForJstree('/api/apply/ipvs/?id='+vip_id,position,parent,'')     
        	$("#modfIpvsVipsubmit").val("vip|"+vip_id)       	
        }
    });	
	
	$(function() {
		if($("#ipvs_vip_project").length){
			$.ajax({
				async : true,  
				url:'/api/project/', //请求地址
				type:"GET",  //提交类似
				success:function(response){
					var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="ipvs_vip_project"  id="ipvs_vip_project" autocomplete="off" onchange="javascript:ipvsVipProjectSelect();"><option selected="selected" value="">请选择一个进行操作</option>'
					var selectHtml = '';
					for (var i=0; i <response.length; i++){
						selectHtml += '<option value="'+ response[i]["id"] +'">'+ response[i]["project_name"] +'</option>' 					 
					};                        
					binlogHtml =  binlogHtml + selectHtml + '</select>';
					$("#ipvs_vip_project").html(binlogHtml)							
					$("#ipvs_vip_project").selectpicker('refresh');							
				}					
			});			
		}	 		
	})		
		
    $('#ipvs_vip_rs').change(function () {
        if ($('#ipvs_vip_rs').val() != "") {
            var span = "<span class='tag' id='span_ipvs_vip_rs'>" + $("#ipvs_vip_rs").find("option:selected").text()
            + "&nbsp;&nbsp;<input name='ipvs_vip' type='hidden' value='"
            + $('#ipvs_vip_rs').val() + "'/></span> &nbsp;";
            if ($("#span_ipvs_vip_rs").length == 0) {
                $('#divSelectedType').append(span);
                
            }
            else {
                $("#span_ipvs_vip_rs").html($("#ipvs_vip_rs").find("option:selected").text()
                 + "&nbsp;&nbsp;<input name='ipvs_vip' type='hidden' value='"
                 + $('#ipvs_vip_rs').val() + "'/></span> &nbsp;");
            }
        }else{
        	$("#span_ipvs_vip_rs").remove()
        }
        changepage(1);
    })  
    
    $('#ipvs_sip').change(function () {
        if ($('#ipvs_sip').val() != "") {
            var span = "<span class='tag' id='span_ipvs_sip'>" + $("#ipvs_sip").find("option:selected").text()
            + "&nbsp;&nbsp;<input name='rs_assets' type='hidden' value='"
            + $('#ipvs_sip').val() + "'/></span> &nbsp;";
            if ($("#span_ipvs_sip").length == 0) {
                $('#divSelectedType').append(span);
                
            }
            else {               
                $("#span_ipvs_sip").html($("#ipvs_sip").find("option:selected").text()
                 + "&nbsp;&nbsp;<input name='rs_assets' type='hidden' value='"
                 + $('#ipvs_sip').val() + "'/></span> &nbsp;");
            }
        }else{
        	$("#span_ipvs_sip").remove()
        }
        changepage(1);
    })     

    $('#ipvs_vip_ns').change(function () {
        if ($('#ipvs_vip_ns').val() != "") {
        	let url = '/api/apply/ipvs/ns/?ipvs_vip='+ $('#ipvs_vip_ns').val()
        	RefreshNameServerTable('ipvsVipAllNameServerManageListTable', url);
        }
    })     
    
	if($("#ipvs_vip_rs").length || $("#ipvs_vip").length){
		var dataList = requests('get','/api/apply/ipvs/')
		IpvsVipSelect("ipvs_vip_rs",dataList["results"]) 
		IpvsVipSelect("ipvs_vip_ns",dataList["results"])
		IpvsVipSelect("ipvs_vip",dataList["results"]) 
		makeipvsVipManageTableList(dataList["results"])	
	}		
	
	if($("#ipvs_sip").length){
		var dataList = requests('get','/api/apply/ipvs/rs/assets/')
		AssetsSelect("ipvs_sip",dataList)
	}		
	
	
	if($("#ipvsVipAllNameServerManageListTable").length){
	    $("button[name^='ns_page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshNameServerTable('ipvsVipAllNameServerManageListTable', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	    makeipvsNameServerManageTableList('ipvsVipAllNameServerManageListTable','/api/apply/ipvs/ns/')  
	}
	
	
	if($("#ipvsRSManageListTable").length){
	    $("button[name^='rs_page_']").on("click", function(){
	      	var url = $(this).val();
	      	$(this).attr("disabled",true);
	      	if (url.length){
	      		RefreshRealServerTable('ipvsRSManageListTable', url);
	      	}      	
	    	$(this).attr('disabled',false);
	      }); 			
	    makeipvsRealServerManageTableList('ipvsRSManageListTable','/api/apply/ipvs/rs/')  
	}
		
  
    $('#ipvsRSManageListTable tbody').on('click', 'td.details-control', function () {
    	var table = $('#ipvsRSManageListTable').DataTable();
    	var dataList = [];
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        aId = row.data()["id"];
        $.ajax({
            url : "/api/apply/ipvs/rs/?id="+aId,
            type : "get",
            async : false,
            success : function(result) {             
            	try {
            		dataList = result.results[0];
            		}
        		catch(error) {
        			dataList = {};
        		  console.error(error);
        		}            	
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
  
    
	$('#ipvsVIPManageListTable tbody').on('click',"button[name='btn-vip-edit']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	let vip =  td.eq(1).text()
    	let scheduler =  td.eq(4).text()    	
    	let protocol =  td.eq(3).text() 
    	let persistence =  td.eq(6).text()
    	let line =  td.eq(7).text()
    	let desc =  td.eq(8).text()  
		switch(protocol)
		{
		    case "TCP":
		    	var protocolOption = '<option selected="selected" value="-t">TCP</option><option value="-u">UDP</option>'
		        break;
		    case "UDP":
		    	var protocolOption = '<option value="-t">TCP</option><option selected="selected" value="-u">UDP</option>'
		        break;		        
		    default:
		    	var protocolOption = '<option value="-t">TCP</option><option value="-u">UDP</option>'
		}    	
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改IPVS: <strong>'+ vip +'</strong>配置',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">协议<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
							 '<select class="form-control" name="protocol">'+
							  protocolOption +	
							 '</select>' +
			              '</div>' +
			            '</div>' +				            
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">调度算法<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			            	makeDynamicSelect(["sh","rr","wrr","lc","wlc"],'scheduler',scheduler) +
			              '</div>' +
			            '</div>' +			            
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">持久化<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              	'<input type="text" class="form-control" placeholder="填入数字(单位秒)" name="persistence" value="'+ persistence  +'" required="required"/>' +
			              '</div>' +
			            '</div>' + 
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">线路<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              	'<input type="text" class="form-control" placeholder="电信|联通|移动" name="line" value="'+ line  +'" required="required"/>' +
			              '</div>' +
			            '</div>' + 	
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">备注<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              	'<input type="text" class="form-control" placeholder="备注" name="desc" value="'+ desc  +'" required="required"/>' +
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
				            url:"/api/apply/ipvs/"+vIds+'/',  
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
					            switch(ipvs_vip_table_type["key"]) {
						            case 'service':
						            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/tree/service/'+ ipvs_vip_table_type["id"] +'/')
						               	break;
						            case 'vip':
						            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/?id='+ ipvs_vip_table_type["id"])
						               	break;
						            default:
						            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')		
					            } 					            
					            		            	
				            }  
				    	});
	                }
	            }
	        }
	    });
    });	
	
	$('#ipvsVIPManageListTable tbody').on('click',"button[name='btn-vip-add']",function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var node =  td.eq(0).text()
    	var port =  td.eq(1).text()
		var dataList = requests('get','/api/apply/ipvs/?id='+vIds)
		IpvsVipSelect("ipvs_vip",dataList["results"],vIds) 
		$("#add_ipvs_rs").val(vIds)
    	$("#add_ipvs_rs_task").show()
    	$("#ipvs_ns").show()
		$.ajax({
			async : true,  
			url:'/api/project/', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="ipvs_rs_project"  id="ipvs_vip_project" autocomplete="off" onchange="javascript:ipvsRealServerProjectSelect();"><option selected="selected" value="">请选择一个项目</option>'
				var selectHtml = '';
				for (var i=0; i <response.length; i++){
					selectHtml += '<option value="'+ response[i]["id"] +'">'+ response[i]["project_name"] +'</option>' 					 
				};                        
				binlogHtml =  binlogHtml + selectHtml + '</select>';
				$("#ipvs_rs_project").html(binlogHtml)							
				$("#ipvs_rs_project").selectpicker('refresh');							
			}					
		});
	})
    
	$('#ipvsVIPManageListTable tbody').on('click',"button[name='btn-vip-rs']",function(){
    	var vIds = $(this).val();
    	$("#ipvs_vip_realserver_detail").show()
        if ($('#ipvsVipRealServerManageListTable').hasClass('dataTable')) {
            dttable = $('#ipvsVipRealServerManageListTable').dataTable();
            dttable.fnClearTable(); 
            dttable.fnDestroy(); 
        }	
    	makeipvsRealServerManageTableList('ipvsVipRealServerManageListTable','/api/apply/ipvs/rs/?ipvs_vip='+vIds)
	})	
	
	$('#ipvsVIPManageListTable tbody').on('click',"button[name='btn-vip-delete']",function(){
		var vIds = $(this).val();  
    	var td = $(this).parent().parent().parent().find("td")
    	var node =  td.eq(1).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>VIP: </strong> <code>' + node + '</code>?',
		    type: 'red',
		    buttons: {
		             删除: function () {		       
				$.ajax({
					url:"/api/apply/ipvs/"+vIds+'/', 
					type:"DELETE",  		
					data:{
						"ipvs_vip":vIds,
					}, 
					success:function(response){
		            	new PNotify({
		                    title: 'Success!',
		                    text: '修改成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')
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

    $("#addIpvsVipsubmit").on('click', function() {
    	var form = document.getElementById('addIpvsVipForm');
    	var post_data = {};
    	var arr = ["line", "desc"];
    	for (var i = 1; i < form.length; ++i) {
    		var name = form[i].name;
    		var value = form[i].value;
    		if (value.length==0 && name.length > 0 && arr.indexOf(name) != -1){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 
    			return false;
    		}else if(name.length > 0 && value.length > 0){
    			post_data[name] = value
    		}
    	};
    	$.ajax({  
            type: "POST",             
            url:"/api/apply/ipvs/",  
            data:post_data,
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
            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')
            }  
    	}); 	
    });		
	
    $("#modfIpvsVipsubmit").on('click', function() {
    	var typeValue = $(this).val()
    	var form = document.getElementById('modfIpvsVipForm');
    	var arr = ["line", "desc"];
    	for (var i = 1; i < form.length; ++i) {
    		var name = form[i].name;
    		var value = form[i].value;
    		if (value.length==0 && name.length > 0 && arr.indexOf(name) != -1){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 
    			return false;
    		}
    	};
    	$.ajax({  
            type: "PUT",             
            url:"/apply/ipvs/vip/batch/",  
            data:$("#modfIpvsVipForm").serialize(),
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
            	if(typeValue.length){
            		var typeValueArray = typeValue.split("|")
					switch(typeValueArray[0])
					{
					    case "service":
					    	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/tree/service/'+typeValueArray[1]+'/')
					        break;
					    case "vip":
					    	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/?id='+typeValueArray[1])
					        break;					    	
					}
            	}else{
            		RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')
            	}
            	
            }  
    	}); 	
    });    
    
    $('#add_ipvs_rs').on('click', function() {
    	var ids = $(this).val()
    	var form = document.getElementById('addIpvsRsForm');
    	var post_data = {};
    	for (var i = 2; i < form.length; ++i) {
    		var name = form[i].name;
    		var value = form[i].value;
    		if (value.length==0 && name.length > 0){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 
    			return false;
    		}else if(name.length > 0 && value.length > 0){
    			post_data[name] = value
    		}
    	};
    	$.ajax({  
            type: "POST",             
            url:"/api/apply/ipvs/rs/",  
            data:post_data,
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                });       
            },  
            success: function(response) {  
//            	console.log(response)
            	new PNotify({
                    title: 'Success!',
                    text: '添加成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshVipTable('#ipvsVIPManageListTable', '/api/apply/ipvs/')
		        if ($('#ipvsVipRealServerManageListTable').hasClass('dataTable')) {
		        	RefreshRealServerTable('ipvsVipRealServerManageListTable', '/api/apply/ipvs/rs/?ipvs_vip='+ids)
		        }            	
            	
            }  
    	});    	
    });    
    
    
	$('#ipvsRSManageListTable tbody').on('click',"button[name='btn-realserver-edit']",function(){
    	var vIds = $(this).val();
    	try {
    		  var data = requests('get',"/api/apply/ipvs/rs/"+vIds+"/")
    		}
		catch(error) {
		  console.error(error);
		  return false
		}
    	var td = $(this).parent().parent().parent().find("td")
    	let ipvs_fw_ip = td.eq(2).text() 
    	let forword = td.eq(3).text() 
		switch(forword)
		{
		    case "NAT":
		    	var forwordOption =	'<option selected="selected" value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option>'
		        break;
		    case "DR":
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option selected="selected" value="-g">DR</option>'
		        break;
		    case "TUN":
		    	var forwordOption = '<option value="-m">NAT</option><option selected="selected" value="-i">TUN</option><option value="-g">DR</option>'
		        break;		    
		    case "FULLNAT":
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option><option selected="selected" value="-b">FULLNAT</option>'
		        break;			        
		    default:
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option>'
		} 		
		var contentHtml = '<form role="form" name="modfSchedrealServerForm" data-parsley-validate class="form-horizontal form-label-left">' +
							'<fieldset>' +	
							'<div class="item form-group">'+
							  '<label class="col-sm-2 control-label">调度类型</label>'+
							  '<div class="col-sm-8">'+
							  '<select class="form-control" name="forword">'+
							 	forwordOption +	
							  '</select>' +
							  '</div>'+
							 '</div>'+								
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">权重</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text"  class="form-control" id="weight" name="weight" placeholder="权重" value="'+ data["weight"] +'" class="input-xlarge"></input>'+
								 '</div>'+
							'</div>'+								
							'</fieldset>'+									 		
						   '</form>'		
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改RealServer: <strong>'+ ipvs_fw_ip +'</strong>',
	        content: contentHtml,
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	            		var realServerForm = this.$content.find('input,select');                	
	            		for (var i = 0; i < realServerForm.length; ++i) {
	            			var name =  realServerForm[i].name
	            			var value = realServerForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/apply/ipvs/rs/"+vIds+'/', 
				            dataType: "json",
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
								RefreshRealServerTable('ipvsRSManageListTable', '/api/apply/ipvs/rs/?'+$.param(ipvs_rs_table_type))
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#ipvsRSManageListTable tbody').on('click',"button[name='btn-realserver-delete']",function(){
		var vIds = $(this).val();  
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>RealServer</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/apply/ipvs/rs/"+vIds+'/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
			            RefreshRealServerTable('ipvsRSManageListTable', '/api/apply/ipvs/rs/')											
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
		

	$('#ipvsVipRealServerManageListTable tbody').on('click',"button[name='btn-realserver-edit']",function(){
    	var vIds = $(this).val();
    	try {
    		  var data = requests('get',"/api/apply/ipvs/rs/"+vIds+"/")
    		}
		catch(error) {
		  console.error(error);
		  return false
		}
    	var td = $(this).parent().parent().parent().find("td")
    	let ipvs_vip = td.eq(1).find("span").attr("title")		
    	let forword = td.eq(3).text() 
		switch(forword)
		{
		    case "NAT":
		    	var forwordOption =	'<option selected="selected" value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option>'
		        break;
		    case "DR":
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option selected="selected" value="-g">DR</option>'
		        break;
		    case "TUN":
		    	var forwordOption = '<option value="-m">NAT</option><option selected="selected" value="-i">TUN</option><option value="-g">DR</option>'
		        break;		    
		    case "FULLNAT":
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option><option selected="selected" value="-b">FULLNAT</option>'
		        break;			        
		    default:
		    	var forwordOption = '<option value="-m">NAT</option><option value="-i">TUN</option><option value="-g">DR</option>'
		} 		
		var contentHtml = '<form role="form" name="modfSchedrealServerForm" data-parsley-validate class="form-horizontal form-label-left">' +
							'<fieldset>' +	
							'<div class="item form-group">'+
							  '<label class="col-sm-2 col-xs-12 control-label">调度类型</label>'+
							  '<div class="col-sm-8">'+
							  '<select class="form-control" name="forword">'+
							 	forwordOption +	
							  '</select>' +
							  '</div>'+
							 '</div>'+								
							'<div class="item form-group">'+
								 '<label class="col-sm-2 control-label">权重</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text"  class="form-control" id="weight" name="weight" placeholder="权重" value="'+ data["weight"] +'" class="input-xlarge"></input>'+
								 '</div>'+
							'</div>'+								
							'</fieldset>'+									 		
						   '</form>'		
    	let ipvs_fw_ip = td.eq(2).text() 
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改RealServer: <strong>'+ ipvs_fw_ip +'</strong>',
	        content: contentHtml,
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	            		var realServerForm = this.$content.find('input,select');                	
	            		for (var i = 0; i < realServerForm.length; ++i) {
	            			var name =  realServerForm[i].name
	            			var value = realServerForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/apply/ipvs/rs/"+vIds+'/', 
				            dataType: "json",
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
								RefreshRealServerTable('ipvsVipRealServerManageListTable', '/api/apply/ipvs/rs/?ipvs_vip='+ipvs_vip)
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#ipvsVipRealServerManageListTable tbody').on('click',"button[name='btn-realserver-delete']",function(){
		var vIds = $(this).val(); 
		var td = $(this).parent().parent().parent().find("td")
		let ipvs_vip = td.eq(1).find("span").attr("title")
		var name = td.eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content: '删除RealServer: <strong>'+ name +'</strong>',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/apply/ipvs/rs/"+vIds+'/', 
					type:"DELETE",  		
					data:{
						"id":vIds,
					}, 
					success:function(response){
			            RefreshRealServerTable('ipvsVipRealServerManageListTable', '/api/apply/ipvs/rs/?ipvs_vip='+ipvs_vip)											
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
	
    $('#add_ipvs_ns').on('click', function() {
    	$.ajax({  
            type: "POST",             
            url:"/api/apply/ipvs/ns/",  
            data:$("#addIpvsNsForm").serialize(),
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
            }  
    	});    	
    }); 
 

	$('#ipvsVipAllNameServerManageListTable tbody').on('click',"button[name='btn-nameserver-edit']",function(){
		var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	let nameserver = td.eq(2).text() 	
		let desc = td.eq(3).text()		
		var contentHtml = '<form role="form" class="form-horizontal form-label-left">' +
							'<fieldset>' +	
							'<div class="form-group">'+
								 '<label class="col-sm-2 control-label">域名</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text"  class="form-control"  name="nameserver" placeholder="域名" value="'+ nameserver +'" class="input-xlarge"></input>'+
								 '</div>'+
							'</div>'+								
							'<div class="form-group">'+
								 '<label class="col-sm-2 control-label">备注</label>'+
								 '<div class="col-sm-8">'+
								 	'<input type="text"  class="form-control"  name="desc" placeholder="备注" value="'+ desc +'" class="input-xlarge"></input>'+
								 '</div>'+
							'</div>'+								
							'</fieldset>'+									 		
						   '</form>'							
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改NameServer: <strong>'+ nameserver +'</strong>',
	        content: contentHtml,
	        keyboardEnabled : true,
	        modal : true,
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                	var formData = {};	
	            		var realServerForm = this.$content.find('input');                	
	            		for (var i = 0; i < realServerForm.length; ++i) {
	            			var name =  realServerForm[i].name
	            			var value = realServerForm[i].value 
	            			if (name.length >0 && value.length > 0){
	            				formData[name] = value	
	            			};		            						
	            		};	
				    	$.ajax({  
				            type: "PUT",  
				            url:"/api/apply/ipvs/ns/"+vIds+'/', 
				            dataType: "json",
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
								RefreshRealServerTable('ipvsVipAllNameServerManageListTable', '/api/apply/ipvs/ns/')
				            }  
				    	});
	                }
	            }
	        }
	    });
    });
	
	$('#ipvsVipAllNameServerManageListTable tbody').on('click',"button[name='btn-nameserver-delete']",function(){	
		var vIds = $(this).val();
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>RealServer</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/apply/ipvs/ns/"+vIds+'/', 
					type:"DELETE",  		
					success:function(response){
			            RefreshRealServerTable('ipvsVipNameServerManageListTable', '/api/apply/ipvs/ns/')											
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
	
	$('#ipvsVipNameServerManageListTable tbody').on('click',"button[name='btn-nameserver-delete']",function(){
		var vIds = $(this).val();
    	try {
  		  var data = requests('get',"/api/apply/ipvs/ns/"+vIds+"/")
  		}
		catch(error) {
		  console.error(error);
		  return false
		}		
		var name = $(this).parent().parent().parent().find("td").eq(2).text()
		$.confirm({
		    title: '删除确认',
		    content: '<strong>RealServer</strong> <code>' + name + '</code>?',
		    type: 'red',
		    buttons: {
		        删除: function () {		       
				$.ajax({
					url:"/api/apply/ipvs/ns/"+vIds+'/', 
					type:"DELETE",  		
					success:function(response){
			            RefreshRealServerTable('ipvsVipNameServerManageListTable', '/api/apply/ipvs/ns/?ipvs_vip='+data["ipvs_vip"])											
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
    
    $("#vipsVipRealtimeStatus").on("click", function(){
    	var data = $(this).val();
    	let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    	var ws_path = ws_scheme + '://' + window.location.host + '/ws/ipvs/stats/'+ data.split("|")[1] + '/' + randromChat + '/';
    	let term =  new Terminal({
    	      cols: 92,
    	      rows: 22,
    	      cursorBlink: false, // 光标闪烁
    	      cursorStyle: 'bar', // 光标样式  null | 'block' | 'underline' | 'bar'
    	      scrollback: 800, //回滚
    	      tabStopWidth: 8, //制表宽度
    	      screenKeys: false// 		
    	});    
    	websocket = make_terminal(term,document.getElementById('webssh_tt'),ws_path,JSON.stringify({"id":data.split("|")[1],"action":data.split("|")[0],"status":"open"})); 
	    $(this).attr("disabled",true);
      });     
    
    $('.bs-example-modal-vip-status').on('hidden.bs.modal', function () {
		try {
			websocket["socket"].close()
		}
		catch(err) {
			console.log(err)
		} 
		finally {
			webssh = false
		}    	
    	$("#vipsVipRealtimeStatus").attr("disabled",false);
    }); 	
	
})