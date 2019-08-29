var userInfo = {
	"0":{"username":"继承上级"}	
}


var webssh = false
function make_terminal(element, size, ws_url) { 
    var term = new Terminal({
        cols: size.cols,
        rows: size.rows,
        screenKeys: true,
        useStyle: true,
        cursorBlink: true,  // Blink the terminal's cursor
    });         	
    if (webssh) {
        return;
    }        
    webssh = true;        	
    term.open(element, false);
    term.write('正在连接...')
/*             term.fit(); */
    var ws = new WebSocket(ws_url);
    ws.onopen = function (event) {
        term.resize(term.cols, term.rows);
/*                 ws.send(JSON.stringify(["id", id,term.cols, term.rows]));  */
        term.on('data', function (data) {
            <!--console.log(data);-->
             ws.send(data); 
        });

        term.on('title', function (title) {
            document.title = title;
        });
        ws.onmessage = function (event) {
        	term.write(event.data);
        };      
    };
    ws.onerror = function (e) {
    	term.write('\r\n连接失败')
    	ws = false
    };
/*    ws.onclose = function () {
        term.destroy();
    }; */     
    return {socket: ws, term: term};
}

var assets_table_id = ''

function format (dataList) {
    var trHtml = '';
	for (var i=0; i <dataList["astList"].length; i++){	
	    trHtml += '<tr><td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["astList"][i]["name"] +':</td>'+ '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["astList"][i]["value"] +'</td></tr>'	    
	};	
	var nktTrHtml = '';
    if (dataList["nktList"].length){
    	var nktTdHtml = '';
		for (var i=0; i <dataList["nktList"].length; i++){	
			if ( dataList["nktList"][i]["status"]=="1"){
				var status = '<span class="label label-success">on</span>' 
			}else{
				var status = '<span class="label label-danger">off</span>'
			}
			nktTdHtml += '</tr>' + 
						 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["name"] +'</td>'+ 
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["mac"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["ipv4"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["speed"] +'</td>' +
					  	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ dataList["nktList"][i]["mtu"] +'</td>' +
					   	 '<td class="col-md-1 col-sm-12 col-xs-12">'+ status +'</td>' +
					   	 '</tr>'
		};	   
		nktTrHtml += nktTrHtml + nktTdHtml 
    }
	var nHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    			'<legend>网卡信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				'<tr>' +
	    					'<th>Name</th>' +
	    					'<th>MAC</th>' +
	    					'<th>IPV4</th>' +
	    					'<th>Speed</th>' +
	    					'<th>MTU</th>' +
	    					'<th>Status</th>' +
	    				'</tr>' + nktTrHtml  +
	    				'</table>'
				'</div>'; 	
		
	    var vHtml = '<div class="col-md-6 col-sm-12 col-xs-12">' +
	    			'<legend>硬件信息</legend>' +
	    				'<table class="table table-striped" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+ 
	    				 trHtml  +
	    				'</table>'
				'</div>'; 				
    return '<div class="row">'+ vHtml + '</div>' + nHtml + '</div>';
}

function RefreshAssetsTable(tableId, urlData){
	$.getJSON(urlData, null, function( dataList ){
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

function updateAssetsByAnsible(dataList,ids){
	var serverId = [];
	for (var i=0; i <dataList.length; i++){
		serverId.push(dataList[i]["id"])
	}
	$.ajax({
		  type: 'POST',
		  url: '/assets/batch/',
		  dataType:"json",
		  data:{
			  'ids':serverId,
			  'model':'batch'
		  },
	      success:function(response){	
	    	var sip = '';
	    	var fip = '';
	    	var modal = '';
    		for  (var i = 0; i < response['data']['success'].length; i++){
    			 sip += response['data']['success'][i] + '<br>'
    		}
    		for  (var i = 0; i < response['data']['failed'].length; i++){
    			 fip += response['data']['failed'][i] + '<br>'
    		}	
    		msg = '成功：'+ '<br>' + sip + '<br>' + '失败：'+ '<br>' + fip;	
	    	if (response['code']==200){
            	new PNotify({
                    title: 'Success!',
                    text: msg,
                    type: 'success',
                    styling: 'bootstrap3',
                    delay: 18000
                }); 
            	RefreshAssetsTable("businessLastNodesAssetsTableLists", "/api/business/nodes/assets/"+ids+"/")
	    	}
	    	else{
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response["msg"],
                    type: 'error',
                    styling: 'bootstrap3',
                    delay: 18000
                }); 
	    	}	            
	      },
        error:function(response){
	      	new PNotify({
	              title: 'Ops Failed!',
	              text: '资产修改失败',
	              type: 'error',
	              styling: 'bootstrap3'
	          }); 
        }
	});			
}


function makeSelect(ids,key,name,dataList){
	var userHtml = '<select required="required" class="form-control" name="'+ name +'" autocomplete="off">'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i][key] +'</option>' 					 
	};                        
	userHtml =  userHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML = userHtml;	
}

function makeAssetsSelectpicker(ids,key,name,dataList){
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]["detail"][key] +'</option>' 					 
	};                        
	selectHtml =  selectHtml + '</select>';
	document.getElementById(ids).innerHTML = selectHtml;
	$("#"+ids).selectpicker('refresh');
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


function InitDataTable(tableId,dataList,buttons,columns,columnDefs,select){
	var dataTableStayle = {
		    "dom": "Bfrtip",
		    "buttons":buttons,
    		"bScrollCollapse": false, 				
    	    "bRetrieve": true,			
    		"destroy": true, 
    		"data":	dataList,
    		"pageLength": 50,
    		"columns": columns,
    		"columnDefs" :columnDefs,
    		"language" : language,
    		"autoWidth": false	    			
		}	
	switch(select) {
	    case "multi":
	    	dataTableStayle["select"] = {
            	"style": 'multi',
                "selector": 'td:first-child'	    			
    		}
	       break;
	    case "os":
	    	dataTableStayle["select"] =	{
            	"style": 'os',
                "selector": 'td:first-child'	    			
    		}
	       break;
	} 	
	oOverviewTable =$('#'+tableId).dataTable(dataTableStayle);
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

function RefreshUserInfo(dataList){
	for (var i=0; i <dataList.length; i++){
		userInfo[dataList[i]["id"]] = dataList[i]
	}		
}

//function RefreshEnvInfo(dataList){
//	for (var i=0; i <dataList.length; i++){
//		envInfo[dataList[i]["id"]] = dataList[i]
//	}		
//}

function abolishAssetBind(select_node,dataList){
  	$.confirm({
  	    title: '确认取消资产关联?',
  	    type: 'red',
  	    content: "取消业务【"+ select_node["paths"] +"】与选定资产关联",
  	    buttons: {
  	        确认: function () {
				let formData = new FormData();
				for (var i = 0; i < dataList.length; ++i) {
					formData.append('assets', dataList[i]["id"]);
				};	            	            
				$.ajax({  
					cache: true,  
					type: "DELETE",  
					url:"/api/business/nodes/assets/"+select_node["id"]+"/",  
					data:formData,
					processData: false,
					contentType: false,	
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
							text: '资产分配成功',
							type: 'success',
							styling: 'bootstrap3'
						}); 
						RefreshAssetsTable("businessLastNodesAssetsTableLists", "/api/business/nodes/assets/"+select_node["id"]+"/")
					}  
				});		        
  	        },
  	       	 取消: function () {
  	            return true;
  	        },
  	    }
  	}); 	
}

function create_nodes(obj,inst){
	var userList = requests("get","/api/user/")
	var userHtml = '<select required="required" class="form-control" name="manage"  autocomplete="off">'
	var userSelectHtml = '<option value="0">继承</option>';
	for (var i=0; i <userList.length; i++){
		userSelectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 						 
	};  
	userHtml =  userHtml + userSelectHtml + '</select>';	
    $.confirm({
        icon: 'fa fa-plus',
        type: 'green',
        title: '添加数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +				          
		            '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称 <span class="required">*</span>' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="text" value="" required="required" class="form-control col-md-7 col-xs-12">' +
		            '</div>' +
		          '</div>' +
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">所属部门 ' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="group" value="" required="required" class="form-control col-md-7 col-xs-12">' +
		            '</div>' +
		          '</div>' +			          
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              userHtml +
		            '</div>' +
		          '</div>' + 
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">描述 <span class="required">*</span>' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="desc" value="" required="required" class="form-control col-md-7 col-xs-12">' +
		            '</div>' +
		          '</div>' +			          
		        '</form>',
        buttons: {
            '取消': function() {},
            '添加': {
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
					formData["parent"] = obj.original["id"]
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:'/api/business/nodes/',  
			            data:formData,
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
			                    text: '业务添加成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	inst.create_node(obj, data, "last")
			            	RefreshTable('businessEnvTableLists', '/api/business/env/')
			            }  
			    	});
                }
            }
        }
    })         	
}

function modf_nodes(obj,inst){
	var userList = requests("get","/api/user/")
	var userHtml = '<select required="required" class="form-control" name="manage"  autocomplete="off">'
	var userSelectHtml = '<option value="0">继承</option>';
	for (var i=0; i <userList.length; i++){
		if (obj.original["manage"]==userList[i]["id"]){
			userSelectHtml += '<option selected="selected" value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>'
		}else{
			userSelectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>'
		}
		 						 
	};  
	userHtml =  userHtml + userSelectHtml + '</select>';	
    $.confirm({
        icon: 'fa fa-plus',
        type: 'blue',
        title: '修改数据',
        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +				          
		            '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称 <span class="required">*</span>' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="text" value="'+ obj.original["text"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
		            '</div>' +
		          '</div>' +
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">所属部门 ' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="group" value="'+ obj.original["group"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
		            '</div>' +
		          '</div>' +			          
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              userHtml +
		            '</div>' +
		          '</div>' + 
		          '<div class="form-group">' +
		            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">描述 <span class="required">*</span>' +
		            '</label>' +
		            '<div class="col-md-6 col-sm-6 col-xs-12">' +
		              '<input type="text"  name="desc" value="'+ obj.original["desc"] +'" required="required" class="form-control col-md-7 col-xs-12">' +
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
			            cache: true,  
			            type: "PUT",  
			            url:'/api/business/nodes/'+obj.original["id"]+'/',  
			            data:formData,
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
			                    text: '业务修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	inst.rename_node(obj,data["text"])
			            	resfreshJSTree('#businessTree',requests('get','/api/business/tree/'))
			            	RefreshTable('businessRootTableLists', '/api/business/nodes/')
			            }  
			    	});
                }
            }
        }
    })         	
}

function delete_nodes(obj,inst){
  	$.confirm({
  	    title: '删除确认?',
  	    type: 'red',
  	    content: "<strong>业务线：</strong>"+ obj.original["text"] +"<br><strong>路径：</strong>【"+ obj.original["paths"] +"】<br><strong>提醒：</strong>删除时会一并删除下面的子业务线。",
  	    buttons: {
  	        确认: function () {
  			$.ajax({
  				  type: 'DELETE',
  				  url:'/api/business/nodes/' + obj.original["id"] + '/',
  			      success:function(response){	
		            	new PNotify({
		                    title: 'Success!',
		                    text: '业务删除成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 
		            	inst.delete_node(obj)
		            	RefreshTable('businessRootTableLists', '/api/business/nodes/');		            
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

function business_assets(obj,inst){	
	if(obj.original["last_node"]==0){
		$.alert({
			type: 'red',
		    title: 'Warning!',
		    content: '请在子业务下面分配资产',
		});   		
	}
}

function getAssetsTags(vIds){
	var dataDict = {}
	$.ajax({  
        cache: true, 
        async: false,
        type: "get",  
        url:'/api/tags/',
        success: function(data) {  
        	dataDict['all'] = data
        }
  
	});	
	$.ajax({  
        cache: true, 
        async: false,
        type: "POST",  
        url:'/assets/server/query/',
        data:{
        	"query":'assets_tags',
        	"id":vIds
        },
        async: false,        
        success: function(data) {  
        	dataDict["tags"] = data["data"]
        }
	});	
	for (var i=0; i <dataDict["tags"].length; i++){
		console.log(dataDict["tags"][i]["id"]) 
		var atid = dataDict["tags"][i]["id"]
		for (var x=0; x <dataDict['all'].length; x++){
			var tid = dataDict['all'][x]["id"]
			if (atid == tid){
				dataDict['all'].splice(x,1)
			}
		}
	};	
	console.log(dataDict)
	return dataDict
}

function viewTags(ids,text){
	$("#myTagsModalLabel").html('<h4 class="modal-title" id="myModalLabel"><code>'+ text +'</code>标签分类</h4>')
	$('select[name="doublebox"]').empty();
	$('#taggroupsubmit').val(ids)
	var data = getAssetsTags(ids)
	$('select[name="doublebox"]').doublebox({
        nonSelectedListLabel: '选择标签类型',
        selectedListLabel: '已选择标签',
        preserveSelectionOnMove: 'moved',
        moveOnSelect: false,
        nonSelectedList:data["all"],
        selectedList:data["tags"],
        optionValue:"id",
        optionText:"tags_name",
        doubleMove:true,
      });			
	$('.bs-example-modal-tags-info').modal({backdrop:"static",show:true});
}

var serverList = []
function viewAssets(ids,text){
	$.ajax({  
        cache: true,  
        type: "get",    
        async: false,
        url:"/assets/manage/?id=" + ids + "&model=info",  
        error: function(response) {
        	new PNotify({
                title: 'Ops Failed!',
                text: response.responseText,
                type: 'error',
                styling: 'bootstrap3'
            });       
        },  
        success: function(response) {  	
        	if (Object.keys(response["data"]).length > 0){            		
        		switch (response["data"]["status"])
        		{
            		case 0:
            		  status = '<span class="label label-success">已上线</span>';
            		  break;
            		case 1:
            		  status = '<span class="label label-warning">已下线</span>';
            		  break;
            		case 2:
            		  status = '<span class="label label-default">维修中</span>';
            		  break;
            		case 3:
            		  status = '<span class="label label-info">已入库</span>';
            		  break;
            		case 4:
            		  status = '<span class="label label-primary">未使用</span>';
            		  break;
        		}
        		switch (response["data"]["assets_type"])
        		{
            		case 'server':
            			assets_type = '<strong>物理服务器</strong>';
            		  	break;
            		case 'vmser':
            			assets_type = '<strong>虚拟机</strong>';
            			break;
            		case 'switch':
            			assets_type = '<strong>交换机</strong>';
            			break;
            		case 'route':
            			assets_type = '<strong>路由器</strong>';
            			break;
            		case 'firewall':
            			assets_type = '<strong>防火墙</strong>';
            			break;
            		case 'storage':
            			assets_type = '<strong>存储设备</strong>';
            			break;	
            		case 'printer':
            			assets_type = '<strong>打印机</strong>';
		            	break;	
            		case 'scanner':
            			assets_type = '<strong>扫描仪</strong>';
		            	break;	
            		case 'wifi':
            			assets_type = '<strong>WIFI设备</strong>';
		            	break;				            	
        		}            		
        		var serverLiTags = '';
        		var netcardLiTags = '';
        		var tagliTags = '<li><a href="https://github.com/welliamcao/OpsManage" target="_blank">CMDB</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">ANSIBLE</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Deploy</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Django</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Bootstrap</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">MySQL</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Redis</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">SaltStack</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Python</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">MongoDB</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Docker</a></li>' +
		            			'<li><a href="https://github.com/welliamcao/OpsManage">Kubernetes</a></li>';
        		var ramLiTags = '<p>如何获取服务器<strong>内存</strong>信息:<a href="https://github.com/welliamcao/OpsManage/issues/69">了解一下</a></p>';
        		var diskLiTags = '<p>如何获取服务器<strong>硬盘</strong>信息:<a href="https://github.com/welliamcao/OpsManage/issues/69">了解一下</a></p>';            		
        		var baseLiTags  =  '<table class="table table-striped">' +		                
						                      '<tbody>' +
						                        '<tr>' +
						                          '<td>资产类型 :</td>' +
						                         ' <td>'+ assets_type +'</td>' +
						                          '<td> 资产编号  :</td>' +
						                          '<td>'+ response["data"]["name"] +'</td>' +			                         
						                        '</tr>' +
						                        '<tr>' +
						                          '<td>设备序列号 :</td>' +
						                          '<td>'+ response["data"]["sn"] +'</td>' +
						                          '<td>购买日期 : </td>' +
						                          '<td>'+ response["data"]["buy_time"] +'</td>' +			                          
						                        '</tr>' +		
						                        '<tr>' +
						                          '<td>过保日期 :</td>' +
						                          '<td>'+ response["data"]["expire_date"] +'</td>' +
						                          '<td>管理IP:</td>' +
						                          '<td>'+ response["data"]["management_ip"] +'</td>' +			                          
						                        '</tr>' +
						                        '<tr>' +
						                          '<td>购买人 : </td>' +
						                          '<td>'+ response["data"]["buy_user"] +'</td>' +
						                          '<td>生产制造商  :</td>' +
						                          '<td>'+ response["data"]["manufacturer"] +'</td>' +			                          
						                        '</tr>' +		
						                        '<tr>' +
						                          '<td>设备型号 :</td>' +
						                          '<td>'+ response["data"]["model"] +'</td>' +
						                          '<td>供货商 : </td>' +
						                          '<td>'+ response["data"]["provider"] +'</td>' +			                          
						                        '</tr>' +	
						                        '<tr>' +
						                          '<td>放置区域 :</td>' +
						                          '<td>'+ response["data"]["put_zone"] +'</td>' +
						                          '<td>机柜信息 : </td>' +
						                          '<td>'+ response["data"]["cabinet"] +'</td>' +			                          
						                        '</tr>' +	
						                        '<tr>' +
						                          '<td>设备状态 : </td>' +
						                          '<td>'+ status +'</td>' +
						                          '<td>使用组 :</td>' +
						                          '<td>'+ response["data"]["group"] +'</td>' +			                          
						                        '</tr>' +
						                        '<tr>' +
						                          '<td>所属项目 : </td>' +
						                          '<td>'+ response["data"]["project"] +'</td>' +
						                          '<td>所属应用 : </td>' +
						                          '<td>'+ response["data"]["service"] +'</td>' +			                          
						                        '</tr>' +			                        
						                      '</tbody>' +
						                    '</table>'							
       		
        		if (Object.keys(response["data"]["server"]).length > 0){
            		serverLiTags = '<table class="table table-striped">' +		                
				                      '<tbody>' +
				                        '<tr>' +
				                          '<td>主机名 :</td>' +
				                         ' <td>'+ response["data"]["server"]["hostname"] +'</td>' +
				                          '<td>操作系统:</td>' +
				                          '<td>'+ response["data"]["server"]["system"]+'</td>' +			                         
				                        '</tr>' +
				                        '<tr>' +
				                          '<td>内核版本 :</td>' +
				                          '<td>'+ response["data"]["server"]["kernel"] +'</td>' +
				                          '<td>IP地址 : </td>' +
				                          '<td>'+ response["data"]["server"]["ip"] +'</td>' +			                          
				                        '</tr>' +		
				                        '<tr>' +
				                          '<td>CPU :</td>' +
				                          '<td>'+ response["data"]["server"]["cpu"] +'</td>' +
				                          '<td>CPU个数:</td>' +
				                          '<td>'+ response["data"]["server"]["vcpu_number"] +'</td>' +			                          
				                        '</tr>' +
				                        '<tr>' +
				                          '<td>硬盘大小(GB) : </td>' +
				                          '<td>'+ response["data"]["server"]["disk_total"] +'</td>' +
				                          '<td>Raid类型:</td>' +
				                          '<td>'+ response["data"]["server"]["raid"] +'</td>' +			                          
				                        '</tr>' +		
				                        '<tr>' +
				                          '<td>出口线路 :</td>' +
				                          '<td>'+ response["data"]["server"]["line"] +'</td>' +
				                          '<td>内存容量 (GB): </td>' +
				                          '<td>'+ response["data"]["server"]["ram_total"] +'</td>' +			                          
				                        '</tr>' +	
				                        '<tr>' +
				                          '<td>Swap容量:</td>' +
				                          '<td>'+ response["data"]["server"]["swap"] +'</td>' +
				                          '<td>Selinux : </td>' +
				                          '<td>'+ response["data"]["server"]["selinux"] +'</td>' +			                          
				                        '</tr>' +				                        
				                      '</tbody>' +
				                    '</table>'							          			
        		}
        		if (Object.keys(response["data"]["networkcard"]).length > 0){
        			var trTags = '';
					for (var i=0; i <response["data"]["networkcard"].length; i++){
	                      if (response["data"]["networkcard"][i]["active"]>0){
	                    	  status = '<td><span class="label label-success">on</span></td>' 
	                      }else{
	                    	  status = '<td><span class="label label-danger">off</span></td>'  
	                      }								
						trTags = trTags + '<tr>' +
				                          '<td>'+ response["data"]["networkcard"][i]["device"] +'</td>' +
				                          '<td>'+ response["data"]["networkcard"][i]["macaddress"]+'</td>' +	
					                      '<td>'+ response["data"]["networkcard"][i]["ip"] +'</td>' +
					                      '<td>'+ response["data"]["networkcard"][i]["module"]+'</td>' +			
					                      '<td>'+ response["data"]["networkcard"][i]["mtu"]+'</td>' +
					                       status +
				                        '</tr>';
					};              			
        			netcardLiTags = '<table class="table table-striped">' +		                
				                      '<tbody>' +
				                        '<tr>' +
				                          '<td>Name</td>' +
				                          '<td>MAC</td>' +	
					                      '<td>IPV4</td>' +
					                      '<td>Speed</td>' +			
					                      '<td>MTU</td>' +				
					                      '<td>Status</td>' +			                        	
				                        '</tr>' + trTags +		                        
				                      '</tbody>' +
				                    '</table>'							            			
					
        		}
        		if (Object.keys(response["data"]["ram"]).length > 0){
        			var trTags = '';
					for (var i=0; i <response["data"]["ram"].length; i++){
	                      if (response["data"]["ram"][i]["device_status"]>0){
	                    	  status = '<td><span class="label label-success">on</span></td>' 
	                      }else{
	                    	  status = '<td><span class="label label-danger">off</span></td>'  
	                      }								
						trTags = trTags + '<tr>' +
				                          '<td>'+ response["data"]["ram"][i]["device_model"] +'</td>' +
				                          '<td>'+ response["data"]["ram"][i]["device_volume"]+'</td>' +	
					                      '<td>'+ response["data"]["ram"][i]["device_brand"] +'</td>' +
					                      '<td>'+ response["data"]["ram"][i]["device_slot"]+'</td>' +			
					                       status +
				                        '</tr>';
					};              			
        			ramLiTags = '<table class="table table-striped">' +		                
					                      '<tbody>' +
					                        '<tr>' +
					                          '<td>内存型号</td>' +
					                          '<td>内存容量(GB)</td>' +	
						                      '<td>生产商</td>' +
						                      '<td>Slot</td>' +					
						                      '<td>Status</td>' +			                        	
					                        '</tr>' + trTags +		                        
					                      '</tbody>' +
					                    '</table>' 							            			
					
        		}   
        		if (Object.keys(response["data"]["disk"]).length > 0){
        			var trTags = '';
					for (var i=0; i <response["data"]["disk"].length; i++){
	                      if (response["data"]["disk"][i]["device_status"]>0){
	                    	  status = '<td><span class="label label-success">on</span></td>' 
	                      }else{
	                    	  status = '<td><span class="label label-danger">off</span></td>'  
	                      }								
						trTags = trTags + '<tr>' +
				                          '<td>'+ response["data"]["disk"][i]["device_model"] +'</td>' +
				                          '<td>'+ response["data"]["disk"][i]["device_volume"]+'</td>' +	
				                          '<td>'+ response["data"]["disk"][i]["device_serial"] +'</td>' +
					                      '<td>'+ response["data"]["disk"][i]["device_brand"] +'</td>' +
					                      '<td>'+ response["data"]["disk"][i]["device_slot"]+'</td>' +			
					                       status +
				                        '</tr>';
					};              			
        			diskLiTags = '<div class="block_content">' +
					                    '<table class="table table-striped">' +		                
					                      '<tbody>' +
					                        '<tr>' +
					                          '<td>硬盘型号</td>' +
					                          '<td>硬盘容量</td>' +	
					                          '<td>序列号</td>' +	
						                      '<td>生产商</td>' +
						                      '<td>Slot</td>' +					
						                      '<td>Status</td>' +			                        	
					                        '</tr>' + trTags +		                        
					                      '</tbody>' +
					                    '</table>'							           			
					
        		} 
        		if (Object.keys(response["data"]["tags"]).length > 0){  
        			tagliTags = ''
					for (var i=0; i <response["data"]["tags"].length; i++){
						tagliTags = tagliTags +  '<li><a href="#">'+ response["data"]["tags"][i]["tags_name"] +'</a></li>' 
					};              									           			
        		}            		
        		var divHtml = '<div class="col-md-12 col-sm-12 col-xs-12" '+ ids +'>' +
                '<div class="x_panel">' +
                  '<div class="x_title">' +
                    '<h2><i class="fa fa-bars"></i>资产明细    <code>'+ text +'</code><small>Assets Info</small></h2>' +                   
                    '<div class="clearfix"></div>' +
                  '</div>' +
                  '<div class="x_content">' +	
                    '<div class="col-md-4 col-sm-4 col-xs-12">' +
                        '<p class="text-left">资产标签</p>'+
	                    '<canvas width="300" height="300" id="myCanvas'+ ids + '">' +
		                    '<ul>' + tagliTags +
		                    '</ul>' +
	                   '</canvas>' +
                    '</div>' + 
                    '<div class="col-md-8 col-sm-8 col-xs-12">' + 
	                    '<div class="" role="tabpanel" data-example-id="togglable-tabs">' +
	                      '<ul id="myTab1" class="nav nav-tabs bar_tabs right" role="tablist">' +
	                        '<li role="presentation" class=""><a href="#tab_content44'+ ids + '" role="tab" id="profile-tab4" data-toggle="tab" aria-controls="profile" aria-expanded="false">内存信息</a>' +
	                        '</li>' +	
	                        '<li role="presentation" class=""><a href="#tab_content55'+ ids + '" role="tab" id="profile-tab5" data-toggle="tab" aria-controls="profile" aria-expanded="false">硬盘信息</a>' +
	                        '</li>' +	
	                        '<li role="presentation" class=""><a href="#tab_content33'+ ids + '" role="tab" id="profile-tab3" data-toggle="tab" aria-controls="profile" aria-expanded="false">网卡信息</a>' +
	                        '</li>' +		                        
	                        '<li role="presentation" class=""><a href="#tab_content22'+ ids + '" role="tab" id="profile-tab2" data-toggle="tab" aria-controls="profile" aria-expanded="false">硬件信息</a>' +
	                        '</li>' +	                        
	                        '<li role="presentation" class="active"><a href="#tab_content11'+ ids + '" id="home-tabb" role="tab1" data-toggle="tab" aria-controls="home" aria-expanded="true">基础信息</a>' +
	                        '</li>' +	
                        
	                      '</ul>' +
	                      '<div id="myTabContent2" class="tab-content">' +
	                        '<div role="tabpanel" class="tab-pane fade active in" id="tab_content11'+ ids +'" aria-labelledby="home-tab">' + baseLiTags +
	                        '</div>' +
	                        '<div role="tabpanel" class="tab-pane fade" id="tab_content22'+ ids + '" aria-labelledby="profile-tab">' + serverLiTags +
	                        '</div>' +
	                        '<div role="tabpanel" class="tab-pane fade" id="tab_content33'+ ids + '" aria-labelledby="profile-tab">' + netcardLiTags +
	                        '</div>' +
	                        '<div role="tabpanel" class="tab-pane fade" id="tab_content44'+ ids + '" aria-labelledby="profile-tab">' + ramLiTags +
	                        '</div>' +
	                        '<div role="tabpanel" class="tab-pane fade" id="tab_content55'+ ids + '" aria-labelledby="profile-tab">' + diskLiTags +
	                        '</div>' +									
	                      '</div>' +
                      '</div>' +
                    '</div>' +					
                  '</div>' +
                '</div>' +
              '</div>'   
             var vid = "#assetsInfo"+ ids   
             var index = $.inArray(vid, serverList)
             if (index>=0){
            	 return false
             }else{
            	 $("#assets_detail").prepend(divHtml);	
            	 serverList.push(vid)
             } 
        		   if( ! $('#myCanvas' + ids).tagcanvas({
        			     textColour : 'dark',
        			     outlineColour: '#ff00ff',
        			     outlineThickness : 1,
        			     maxSpeed : 0.03,
        			     depth : 0.75
        			   })) {
        			     // TagCanvas failed to load
        			     $('#myCanvasContainer').hide();
        			   }          		
        	}            	
        }
    });	
}


function customMenu(node) {
    var items = {
            "new":{  
                "label":"添加业务",  
                "icon": "glyphicon glyphicon-plus",
                "action":function(data){
                	var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
                	create_nodes(obj,inst)
                }  
            },
            "modf":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "修改资料",
					"shortcut_label"	: 'F2',
					"icon"				: "glyphicon glyphicon-edit",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						modf_nodes(obj,inst)						
					}
            },
            "del":{
        		"separator_before"	: false,
				"separator_after"	: false,
				"_disabled"			: false, 
				"label"				: "删除业务",
				"shortcut_label"	: 'F2',
				"icon"				: "fa fa fa-remove",
				"action"			: function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);		
					delete_nodes(obj,inst)
				}
            },
        }  
    return items
}

function resfreshJSTree(ids,dataList){ 
	$(ids).jstree(true).settings.core.data = dataList;
	$(ids).jstree(true).refresh();
}
function drawTree(ids,dataList){ 
	$(ids).jstree('destroy');
    $(ids).jstree({	
	    "core" : {
	      "check_callback": function (op, node, par, pos, more) {  	  
	    	    if (op === "move_node" || op === "copy_node") {	    	    	
	    	        return false;
	    	    }
	    	    return true;
	    	},
	      'data' : dataList
	    },	    
	    "plugins": ["contextmenu", "dnd", "search","themes","state", "types", "wholerow","json_data","unique"],
	    'state': {
	             "opened":true,
	     },	    
	    "contextmenu":{
		    	select_node:true,
		    	show_at_node:false,
		    	'items': customMenu
		      }	    
	});	
}




RefreshUserInfo(requests("get","/api/user/"))

var envDataList = requests('get',"/api/business/env/")


$(document).ready(function() {
	
	function makeBusinessRnvTables(envDataList){
//		RefreshUserInfo()
	    var columns = [
	                    {"data": "id"},
	                    {"data": "name"},	
		               ]
	    var columnDefs = [		   	    		                         
   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-business-env-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' + 	    	                           
		    	                           '<button type="button" name="btn-business-env-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addBusinessEnvModal').modal("show");								            	
            }
        }]
			
		InitDataTable('businessEnvTableLists',envDataList,buttons,columns,columnDefs)			
	}  	
		
	makeBusinessRnvTables(envDataList)
	

	$('#businessEnvTableLists tbody').on('click',"button[name='btn-business-env-modf']", function(){
    	var vIds = $(this).val();
		var business = $(this).parent().parent().parent().find("td").eq(1).text();                       		
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">环境类型 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="name" value="'+ business +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' + 		                        
			        '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var param_name = this.$content.find("[name='name']").val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/business/env/" + vIds + '/',  
				            data:{
				            	"name":param_name,
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
				            	RefreshTable('businessEnvTableLists', '/api/business/env/');
				            }  
				    	});
	                }
	            }
	        }
	    });	
    });	
	
	
	//删除项目资产
	$('#businessEnvTableLists tbody').on('click',"button[name='btn-business-env-confirm']", function(){
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
	  				  url:'/api/business/env/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '修改成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('businessEnvTableLists', '/api/business/env/');
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
    
	//添加业务环境资产
    $('#addBusinessEnvSubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/business/env/",  
            data:$('#addBusinessEnvForm').serialize(),
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
            	RefreshTable('businessEnvTableLists', '/api/business/env/');
            }  
    	});  	
    });		
	
	function makeBusinessTreeTables(treeDataList){
//		RefreshEnvInfo()
	    var columns = [
	                    {"data": "id"},
	                    {"data": "text"},
						{"data": "env_name"},						
	                    {"data": "manage_name"},
						{"data": "group"},
						{"data": "paths"},
						{"data": "desc"}
		               ]
	    var columnDefs = [		                                            
   	    		        {
	    	    				targets: [7],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +
	    	                        	   	'<button type="button" name="btn-business-root-tree" value="'+ row.tree_id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
	    	                           		'</button>' + 	    	                        
	    	                           		'<button type="button" name="btn-business-root-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
	    	                           		'</button>' + 	    	                           
	    	                           		'<button type="button" name="btn-business-root-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
            	$('#addBusinessRootModal').modal("show");	
            	makeSelect('businessRootManageSelect','username','manage',requests("get","/api/user/"))
            	makeSelect('businessRootEnvSelect','name','env',requests("get","/api/business/env/"))								            	
            }
        }]
		InitDataTable('businessRootTableLists',treeDataList,buttons,columns,columnDefs)			
	}  	
	
	var treeDataList = requests('get',"/api/business/nodes/")
    
	makeBusinessTreeTables(treeDataList)
	

  //修改项目资产
	$('#businessRootTableLists tbody').on('click',"button[name='btn-business-root-modf']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
		var business = td.eq(1).text(); 
    	var env = td.eq(2).text();
		var manage = td.eq(3).text(); 
		var group = td.eq(4).text(); 
		var desc = td.eq(6).text(); 
    	var userList = requests("get","/api/user/")
		var userHtml = '<select required="required" class="form-control" name="manage"  autocomplete="off">'
		var userSelectHtml = '';
		for (var i=0; i <userList.length; i++){
			if (userList[i]["username"]==manage){
				userSelectHtml += '<option selected="selected" value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 	
			}else{
				userSelectHtml += '<option value="'+ userList[i]["id"] +'">'+ userList[i]["username"] +'</option>' 	
			}						 
		};                        
		userHtml =  userHtml + userSelectHtml + '</select>';	
    	var envList = requests("get","/api/business/env/")
		var envHtml = '<select required="required" class="form-control" name="env"  autocomplete="off">'
		var envSelectHtml = '';
		for (var i=0; i <envList.length; i++){
			if (envList[i]["name"]==env){
				envSelectHtml += '<option selected="selected" value="'+ envList[i]["id"] +'">'+ envList[i]["name"] +'</option>' 	
			}else{
				envSelectHtml += '<option value="'+ envList[i]["id"] +'">'+ envList[i]["name"] +'</option>' 	
			}
							 
		};                        
		envHtml =  envHtml + envSelectHtml + '</select>';		
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改数据',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">环境<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              envHtml +
			            '</div>' +
			          '</div>' +				          
			            '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">名称 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="text" value="'+ business +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">所属部门 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="group" value="'+ group +'" required="required" class="form-control col-md-7 col-xs-12">' +
			            '</div>' +
			          '</div>' +			          
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">负责人<span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              userHtml +
			            '</div>' +
			          '</div>' + 
			          '<div class="form-group">' +
			            '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">描述 <span class="required">*</span>' +
			            '</label>' +
			            '<div class="col-md-6 col-sm-6 col-xs-12">' +
			              '<input type="text"  name="desc" value="'+ desc +'" required="required" class="form-control col-md-7 col-xs-12">' +
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
				            cache: true,  
				            type: "PUT",  
				            url:"/api/business/nodes/" + vIds + '/',  
				            data:formData,
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
				            	RefreshTable('businessRootTableLists', '/api/business/nodes/');
				            }  
				    	});
	                }
	            }
	        }
	    });	
    });	
	
	
	//删除项目资产
	$('#businessRootTableLists tbody').on('click',"button[name='btn-business-root-confirm']", function(){
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
	  				  url:'/api/business/nodes/' + vIds + '/',
	  			      success:function(response){	
			            	new PNotify({
			                    title: 'Success!',
			                    text: '资产删除成功',
			                    type: 'success',
			                    styling: 'bootstrap3'
			                }); 
			            	RefreshTable('businessRootTableLists', '/api/business/nodes/');		            
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

	$('#businessRootTableLists tbody').on('click',"button[name='btn-business-root-tree']", function(){
    	var vIds = $(this).val();
    	drawTree('#businessTree',requests("get","/api/business/tree/?tree_id="+vIds))
    });		
	
	//添加项目资产
    $('#addBusinessRootSubmit').on('click', function() {
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/business/nodes/",  
            data:$('#businessRootForm').serialize(),
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
            	RefreshTable('businessRootTableLists', '/api/business/nodes/');
            }  
    	});  	
    });	
       
	function makeBusinessChildrenNodesTables(treeDataList){
	    var columns = [
	                    {"data": "id"},
	                    {"data": "text"},						
	                    {"data": "manage"},
						{"data": "group"},
						{"data": "paths"},
						{"data": "desc"}
		               ]
	    var columnDefs = [	                      
	   	    		        {
	    	    				targets: [2],
	    	    				render: function(data, type, row, meta) {	
	    	                        return userInfo[row.manage]["username"]
	    	    				},
	    	    				"className": "text-center",
	    		        },	                      
//	    		        {
//	    	    				targets: [6],
//	    	    				render: function(data, type, row, meta) {
//	    	    					if (row.last_node == 1 ){
//	    	    						var database = '<button type="button" name="btn-business-childrenNodes-modf" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-database" aria-hidden="true"></span></button>'
//	    	    						var deleteButton = '<button type="button" name="btn-business-childrenNodes-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span></button>'
//	    	    					}else{
//	    	    						var database = '<button type="button" name="btn-business-childrenNodes-modf" value="" class="btn btn-default"  aria-label="Justify" disabled="disabled"><span class="fa fa-database" aria-hidden="true"></span></button>'
//	    	    						var deleteButton = '<button type="button" name="btn-business-childrenNodes-confirm" value="'+ row.id +'" class="btn btn-default" aria-label="Justify" disabled="disabled"><span class="fa fa-trash" aria-hidden="true"></span></button>'
//	    	    					}
//	    	                        return '<div class="btn-group  btn-group-xs">' +	
//	    	                        		database + deleteButton +	    	                           			                            
//		    	                           '</div>';
//	    	    				},
//	    	    				"className": "text-center",
//	    		        },
	    		      ]	
     var buttons = []
		InitDataTable('businessChildrenNodesTableLists',treeDataList,buttons,columns,columnDefs)			
	}  
	
    function makeAssetsTableList(dataList,select_node){
        var columns = [		                       
    		           {
   		                "orderable": false,
   		                "data":      null,
   		                "className": 'select-checkbox', 
   		                "defaultContent": ''
    		           },  
                       {
						"className": 'details-control',
						"orderable": false,
						"data":      null,
						"defaultContent": ''
                       },	
                       {"data": "assets_type"},		                       
                       {"data": "detail.ip"},     
                       {
                    	   "data": "detail.system",
                    	   "defaultContent": ''
                       },
                       {
                    	   "data": "detail.kernel",
                    	   "defaultContent": ''
    	               },
    	               {
    	            	   "data": "detail.vcpu_number",
    	            	   "defaultContent": ''
    	               },
    	               {
    	            	   "data": "detail.ram_total",
    	            	   "defaultContent": ''
    	               },
    	               {
    	            	   "data": "detail.disk_total",
    	            	   "defaultContent": ''
    	               },
    	               {
    	            	   "data": "put_zone",
    	            	   "defaultContent": ''
    	               }
    	               ]
       var columnDefs = [                      	    		     		    		    	    		    
    	    		        {
       	    				targets: [10],
       	    				render: function(data, type, row, meta) {  
    	                        if(row.assets_type == '服务器'){
		                            var hw = '<button type="button" name="btn-assets-hw" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align"><span class="fa fa-hdd-o" aria-hidden="true"></span></button>'		    	               
    	                        }else{
    	                        	var hw = '<button type="button" name="btn-assets-hw" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align" disabled><span class="fa fa-hdd-o" aria-hidden="true"></span></button>'		    	   
    	                        }       	    					
       	                        return '<div class="btn-group  btn-group-xs">' +	
			       	                     	'<button type="button" name="btn-assets-alter" value="'+ row.id +'" class="btn btn-default" aria-label="Center Align"><a href="/assets/manage/?id='+row.id+'&model=edit" target="view_window"><span class="glyphicon glyphicon-check" aria-hidden="true"></span></a>' +
				                            '</button>' +
				                            '<button type="button" name="btn-assets-info" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align" data-toggle="modal" data-target=".bs-example-modal-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>' +
				                            '</button>' +	                            
				                            '<button type="button" name="btn-assets-update" value="'+ row.id +'" class="btn btn-default" aria-label="Right Align"><span class="glyphicon glyphicon-refresh" aria-hidden="true"></span>' +
				                            '</button>' + hw +
				                            '<button type="button" name="btn-assets-webssh" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-desktop" aria-hidden="true"></span>' +
				                            '</button>'+
				                            '<button type="button" name="btn-assets-detail" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-search" aria-hidden="true"></span>' +
				                            '</button>'+				                            
    	    	                           '</div>';
       	    				},
       	    				"className": "text-center",
    	    		        },
  	    		        
    	    		      ]	
        var buttons = [
            {
               text: '关联',
               className: "btn-sm",
               action: function (e, dt, button, config) {        	
            	let dataList = requests("get","/api/business/nodes/assets/"+ select_node["id"] +"/?type=unallocated")
            	if (dataList.length){
            		makeAssetsSelectpicker("addBusinessAssetsSelect","ip","assets",dataList)
            		$('#addBusinessAssetsModal').modal("show");
            		$("#addBusinessAssetsModalLabel").html('<h4 class="modal-title" id="addBusinessAssetsModalLabel"><code>'+ select_node["paths"] +'</code> 分配资产</h4>')
            		$("#addBusinessAssetsSubmit").val(select_node["id"])         		
            	}else{
            		$.alert({
            		    title: '操作失败',
            		    content: '没有剩余的资产可以进行分配！',
            		    type: 'red',		    
            		});	            		
            	}            	
               }
            },     
            {
                text: '取消',
                className: "btn-sm",
                action: function (e, dt, button, config) {        	
                	let dataList = dt.rows('.selected').data()
                	var vIdsList = new Array();
                	if (dataList.length==0){
                		$.alert({
                		    title: '操作失败',
                		    content: '批量更新资产失败，请先选择资产',
                		    type: 'red',		    
                		});	            		
                	}else{ 
                		abolishAssetBind(select_node,dataList)
                	}                 	
                }
            },             
            {
            	text: '更新',
            	className: "btn-sm",
            	action: function ( e, dt, node, config ) {        	
                	let dataList = dt.rows('.selected').data()
                	var vips = ''
                	if (dataList.length==0){
                		$.alert({
                		    title: '操作失败',
                		    content: '批量更新资产失败，请先选择资产',
                		    type: 'red',		    
                		});	            		
                	}else{ 
                		$.alert({
                		    title: '<i class="fa  fa-spinner  "></i> 操作提醒',
                		    content: '批量更新资产操作耗时较久，请勿重复提交',
                		    type: 'green',		    
                		});	                		
                		updateAssetsByAnsible(dataList,select_node["id"])
                	} 
            	} 
        	},
            {
                text: '修改',
                className: "btn-sm",
                action: function (e, dt, button, config) {
                	//dt.rows().select();          	
                }
            },  
            {
                text: '标签',
                className: "btn-sm",
                action: function (e, dt, button, config) {
                	let dataList = dt.rows('.selected').data()
                	var vips = ''
                	if (dataList.length==1){
                		console.log(dataList)
                		viewTags(dataList[0]["detail"]["assets_id"],dataList[0]["detail"]["ip"])
                	}else{ 
                		$.alert({
                		    title: '操作失败',
                		    content: '资产标签操作失败，请先选择一个资产',
                		    type: 'red',		    
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
    	InitDataTable('businessLastNodesAssetsTableLists',dataList,buttons,columns,columnDefs,'multi');	
    }	
	
    $('#addBusinessAssetsSubmit').on('click', function() {
		var vIds = $(this).val();
    	$.ajax({  
            cache: true,  
            type: "POST",  
            url:"/api/business/nodes/assets/"+vIds+"/",  
            data:$('#addBusinessAssetsForm').serialize(),
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
                    text: '资产分配成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	RefreshAssetsTable("businessLastNodesAssetsTableLists", "/api/business/nodes/assets/"+vIds+"/")
            }  
    	});  	
    });	    
    
    
    if ($('#businessEnvSelect').length){
		let selectHtml = '';
		for (var i=0; i <envDataList.length; i++){
			selectHtml += '<option value="'+ envDataList[i]["id"] +'">'+ envDataList[i]["name"] +'</option>' 					 
		};                        
		selectHtml =  selectHtml + '</select>';
		document.getElementById("businessEnvSelect").innerHTML = selectHtml;
		$("#businessEnvSelect").selectpicker('refresh');
    	
        $('#businessEnvSelect').change(function () {
        	let selectVal = $('#businessEnvSelect').val()
            if (selectVal != "") {
                console.log(selectVal)
                drawTree('#businessTree',requests("get","/api/business/tree/?env="+selectVal)) 
            }
        })    	
    	
    }

    

    
	var treeDataList = requests("get","/api/business/tree/")	
	
	drawTree('#businessTree',treeDataList)   
 
    $("#search-input").keyup(function () {
        var searchString = $(this).val();
        $('#businessTree').jstree('search', searchString);
    });	
	
	$("#businessTree").click(function () {
	     var position = 'last';
	     let select_node = $(this).jstree("get_selected",true)[0]["original"];
	     
	     if (select_node["last_node"] == 0 && select_node["parentId"] > 0){
				$.ajax({
					  type: 'GET',
//查询所有子节点					  url: '/api/business/nodes/?tree_id='+ select_node["tree_id"] +'&lft='+ select_node["lft"] +'&rght='+ select_node["rght"],
					  url: '/api/business/nodes/'+ select_node["id"] +'/?type=children',
				      success:function(response){	
				    	  $("#childrenNodes").show()
				    	  $("#nodesAssets").hide()
				    	  $("#nodeName").html('<h2 id="nodeName">'+ select_node["paths"] +'_子节点 <small>Business Nodes</small></h2>')
				    	  if ($('#businessChildrenNodesTableLists').hasClass('dataTable')) {
				            dttable = $('#businessChildrenNodesTableLists').dataTable();
				            dttable.fnClearTable(); //清空table
				            dttable.fnDestroy(); //还原初始化datatable
				    	  }			    	  
				    	  makeBusinessChildrenNodesTables(response)
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
	     }else if(select_node["last_node"] == 1){
				$.ajax({
					  type: 'GET',
					  url: '/api/business/nodes/assets/'+ select_node["id"] + '/',
				      success:function(response){	
				    	  $("#childrenNodes").hide()
				    	  $("#nodesAssets").show()
				    	  $("#lastNodeName").html('<h2 id="lastNodeName">'+ select_node["paths"] +' <small>Business Nodes Assets</small></h2>')
				    	  if ($('#businessLastNodesAssetsTableLists').hasClass('dataTable')) {
				            dttable = $('#businessLastNodesAssetsTableLists').dataTable();
				            dttable.fnClearTable(); //清空table
				            dttable.fnDestroy(); //还原初始化datatable
				    	  }			    	  
				    	  makeAssetsTableList(response,select_node)
				    	  assets_table_id = select_node["id"]
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

$(document).ready(function() {	    
	
    // Add event listener for opening and closing details
    $('#businessLastNodesAssetsTableLists tbody').on('click', 'td.details-control', function () {
    	var table = $('#businessLastNodesAssetsTableLists').DataTable();
    	var dataList = [];
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        aId = row.data()["id"];
        $.ajax({
            url : "/api/assets/info/"+aId+"/",
            type : "post",
            async : false,
            data : {"id":aId},
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
	
	//更新资产
	$('#businessLastNodesAssetsTableLists tbody').on('click','button[name="btn-assets-update"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
    	var ip = $(this).parent().parent().parent().find("td").eq(3).text(); 
		$.confirm({
		    title: '更新确认',
		    content: ip,
		    type: 'blue',
		    buttons: {
		              更新: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:"/assets/modf/" + vIds + '/', 
			            data:{"model":'setup',"ids":vIds},
			            error: function(request) {  
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: "更新失败",
			                    type: 'error',
			                    styling: 'bootstrap3'
			                });       
			            },  
			            success: function(request) {  
			            	if (request["code"] == "200"){
				            	new PNotify({
				                    title: 'Success!',
				                    text: request["msg"],
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshAssetsTable("businessLastNodesAssetsTableLists", "/api/business/nodes/assets/"+assets_table_id+"/")				            		
			            	}else{
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: request["msg"],
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });  				            		
			            	}

			            }  
			    	});
		        },
			        取消: function () {
			            return true;			            
			        },			        
			    }
		});			
		$(this).attr('disabled',false);
	});
	
	//更新资产
	$('#businessLastNodesAssetsTableLists tbody').on('click','button[name="btn-assets-hw"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
    	var ip = $(this).parent().parent().parent().find("td").eq(3).text(); 
		$.confirm({
		    title: '更新内存硬盘信息',
		    content: ip,
		    type: 'blue',
		    buttons: {
		              更新: function () {
			    	$.ajax({  
			            cache: true,  
			            type: "POST",  
			            url:"/assets/modf/" + vIds + '/', 
			            data:{"model":'crawHw',"ids":vIds},
			            error: function(request) {  
			            	new PNotify({
			                    title: 'Ops Failed!',
			                    text: "更新失败",
			                    type: 'error',
			                    styling: 'bootstrap3'
			                });       
			            },  
			            success: function(request) {  
			            	if (request["code"] == "200"){
				            	new PNotify({
				                    title: 'Success!',
				                    text: request["msg"],
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshAssetsTable("businessLastNodesAssetsTableLists", "/api/business/nodes/assets/"+assets_table_id+"/")				            		
			            	}else{
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: request["msg"],
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });  				            		
			            	}

			            }  
			    	});
		        },
			        取消: function () {
			            return true;			            
			        },			        
			    }
		});			
		$(this).attr('disabled',false);
	});		
	
	$('#businessLastNodesAssetsTableLists tbody').on('click','button[name="btn-assets-webssh"]',function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")	
		$("#myWebsshModalLabel").html('<p class="text-blank"><code><i class="fa fa fa-terminal"></i></code>'+td.eq(3).text()+'</p>')
		$("#websshConnect").val(vIds)	
		$('#webssh_tt').empty()
    	$('.bs-example-modal-webssh-info').modal({backdrop:"static",show:true}); 		
	})	
	
    $("#websshConnect").on("click", function(){
    	var vIds = $(this).val();
    	var randromChat = makeRandomId()
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://' + window.location.host + '/ssh/' + vIds + '/' + randromChat + '/';
//        console.log(randromChat)
        websocket = make_terminal(document.getElementById('webssh_tt'), {rows: 30, cols: 140}, ws_path);  
        $(this).attr("disabled",true);
/*             $(".xterm-screen").css("width", "800px").css("height", "510px"); */
      });  	

    $('.bs-example-modal-webssh-info').on('hidden.bs.modal', function () {
		try {
			websocket["socket"].close()
		}
		catch(err) {
			console.log(err)
		} 
		finally {
			webssh = false
		}    	
    	$("#websshConnect").attr("disabled",false);
    }); 	
	
	$('#businessLastNodesAssetsTableLists tbody').on('click','button[name="btn-assets-detail"]',function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")		
    	viewAssets(vIds,td.eq(3).text())
	})    
    
    $('#businessLastNodesAssetsTableLists tbody').on('click','button[name="btn-assets-info"]',function(){
    		$(this).attr('disabled',true);
    		var vIds = $(this).val();
    		var ip = $("#assets_"+vIds).text(); 
    		$.ajax({  
    	        cache: true,  
    	        type: "GET",  
    	        url:"/assets/manage/?id="+ vIds +"&model=info",  
    	        async: false,  
    	        error: function(response) {  
    	        	console.log(response)
    	        },  
    	        success: function(response) {   	
    	        	if (Object.keys(response["data"]).length > 0){
    	        		switch (response["data"]["status"])
    	        		{
    	            		case 0:
    	            		  status = '<span class="label label-success">已上线</span>';
    	            		  break;
    	            		case 1:
    	            		  status = '<span class="label label-warning">已下线</span>';
    	            		  break;
    	            		case 2:
    	            		  status = '<span class="label label-default">维修中</span>';
    	            		  break;
    	            		case 3:
    	            		  status = '<span class="label label-info">已入库</span>';
    	            		  break;
    	            		case 4:
    	            		  status = '<span class="label label-primary">未使用</span>';
    	            		  break;
    	        		}
    	        		switch (response["data"]["assets_type"])
    	        		{
    	            		case 'server':
    	            			assets_type = '<strong>物理服务器</strong>';
    	            		  	break;
    	            		case 'vmser':
    	            			assets_type = '<strong>虚拟机</strong>';
    	            			break;
    	            		case 'switch':
    	            			assets_type = '<strong>交换机</strong>';
    	            			break;
    	            		case 'route':
    	            			assets_type = '<strong>路由器</strong>';
    	            			break;
    	            		case 'firewall':
    	            			assets_type = '<strong>防火墙</strong>';
    	            			break;
    	            		case 'storage':
    	            			assets_type = '<strong>存储设备</strong>';
    	            			break;	
    	            		case 'printer':
    	            			assets_type = '<strong>打印机</strong>';
    			            	break;	
    	            		case 'scanner':
    	            			assets_type = '<strong>扫描仪</strong>';
    			            	break;	
    	            		case 'wifi':
    	            			assets_type = '<strong>WIFI设备</strong>';
    			            	break;				            	
    	        		}             		
    	        		var ulTag = '<ul class="list-unstyled timeline" id="assets_info">';
    	        		var serverLiTags = '';
    	        		var netcardLiTags = '';
    	        		var ramLiTags = '';
    	        		var diskLiTags = '';            		
    	        		var baseLiTags  =  '<li>' +
    										  '<div class="block">' +
    											'<div class="tags">' +
    											  '<a href="" class="tag">' +
    												'<span>基础信息</span>' +
    											  '</a>' +
    											'</div>' +
    											'<div class="block_content">' +
    							                    '<table class="table table-striped">' +		                
    							                      '<tbody>' +
    							                        '<tr>' +
    							                          '<td>资产类型 :</td>' +
    							                         ' <td>'+ assets_type +'</td>' +
    							                          '<td> 资产编号  :</td>' +
    							                          '<td>'+ response["data"]["name"] +'</td>' +			                         
    							                        '</tr>' +
    							                        '<tr>' +
    							                          '<td>设备序列号 :</td>' +
    							                          '<td>'+ response["data"]["sn"] +'</td>' +
    							                          '<td>购买日期 : </td>' +
    							                          '<td>'+ response["data"]["buy_time"] +'</td>' +			                          
    							                        '</tr>' +		
    							                        '<tr>' +
    							                          '<td>过保日期 :</td>' +
    							                          '<td>'+ response["data"]["expire_date"] +'</td>' +
    							                          '<td>管理IP:</td>' +
    							                          '<td>'+ response["data"]["management_ip"] +'</td>' +			                          
    							                        '</tr>' +
    							                        '<tr>' +
    							                          '<td>购买人 : </td>' +
    							                          '<td>'+ response["data"]["buy_user"] +'</td>' +
    							                          '<td>生产制造商  :</td>' +
    							                          '<td>'+ response["data"]["manufacturer"] +'</td>' +			                          
    							                        '</tr>' +		
    							                        '<tr>' +
    							                          '<td>设备型号 :</td>' +
    							                          '<td>'+ response["data"]["model"] +'</td>' +
    							                          '<td>供货商 : </td>' +
    							                          '<td>'+ response["data"]["provider"] +'</td>' +			                          
    							                        '</tr>' +	
    							                        '<tr>' +
    							                          '<td>放置区域 :</td>' +
    							                          '<td>'+ response["data"]["put_zone"] +'</td>' +
    							                          '<td>机柜信息 : </td>' +
    							                          '<td>'+ response["data"]["cabinet"] +'</td>' +			                          
    							                        '</tr>' +	
    							                        '<tr>' +
    							                          '<td>设备状态 : </td>' +
    							                          '<td>'+ status +'</td>' +
    							                          '<td>使用组 :</td>' +
    							                          '<td>'+ response["data"]["group"] +'</td>' +			                          
    							                        '</tr>' +
    							                        '<tr>' +
    							                          '<td>所属项目 : </td>' +
    							                          '<td>'+ response["data"]["project"] +'</td>' +
    							                          '<td>所属应用 : </td>' +
    							                          '<td>'+ response["data"]["service"] +'</td>' +			                          
    							                        '</tr>' +			                        
    							                      '</tbody>' +
    							                    '</table>' +							
    											'</div>' +
    										  '</div>' +
    										'</li>';
    	        		if (Object.keys(response["data"]["server"]).length > 0){
    	            		serverLiTags = '<li>' +
    						  '<div class="block">' +
    							'<div class="tags">' +
    							  '<a href="" class="tag">' +
    								'<span>硬件信息</span>' +
    							  '</a>' +
    							'</div>' +
    							'<div class="block_content">' +
    			                    '<table class="table table-striped">' +		                
    			                      '<tbody>' +
    			                        '<tr>' +
    			                          '<td>主机名 :</td>' +
    			                         ' <td>'+ response["data"]["server"]["hostname"] +'</td>' +
    			                          '<td>操作系统:</td>' +
    			                          '<td>'+ response["data"]["server"]["system"]+'</td>' +			                         
    			                        '</tr>' +
    			                        '<tr>' +
    			                          '<td>内核版本 :</td>' +
    			                          '<td>'+ response["data"]["server"]["kernel"] +'</td>' +
    			                          '<td>IP地址 : </td>' +
    			                          '<td>'+ response["data"]["server"]["ip"] +'</td>' +			                          
    			                        '</tr>' +		
    			                        '<tr>' +
    			                          '<td>CPU :</td>' +
    			                          '<td>'+ response["data"]["server"]["cpu"] +'</td>' +
    			                          '<td>CPU个数:</td>' +
    			                          '<td>'+ response["data"]["server"]["vcpu_number"] +'</td>' +			                          
    			                        '</tr>' +
    			                        '<tr>' +
    			                          '<td>硬盘大小(GB) : </td>' +
    			                          '<td>'+ response["data"]["server"]["disk_total"] +'</td>' +
    			                          '<td>Raid类型:</td>' +
    			                          '<td>'+ response["data"]["server"]["raid"] +'</td>' +			                          
    			                        '</tr>' +		
    			                        '<tr>' +
    			                          '<td>出口线路 :</td>' +
    			                          '<td>'+ response["data"]["server"]["line"] +'</td>' +
    			                          '<td>内存容量 (GB): </td>' +
    			                          '<td>'+ response["data"]["server"]["ram_total"] +'</td>' +			                          
    			                        '</tr>' +	
    			                        '<tr>' +
    			                          '<td>Swap容量:</td>' +
    			                          '<td>'+ response["data"]["server"]["swap"] +'</td>' +
    			                          '<td>Selinux : </td>' +
    			                          '<td>'+ response["data"]["server"]["selinux"] +'</td>' +			                          
    			                        '</tr>' +				                        
    			                      '</tbody>' +
    			                    '</table>' +							
    							'</div>' +
    						  '</div>' +
    						'</li>';            			
    	        		}
    	        		if (Object.keys(response["data"]["networkcard"]).length > 0){
    	        			var trTags = '';
    						for (var i=0; i <response["data"]["networkcard"].length; i++){
    		                      if (response["data"]["networkcard"][i]["active"]>0){
    		                    	  status = '<td><span class="label label-success">on</span></td>' 
    		                      }else{
    		                    	  status = '<td><span class="label label-danger">off</span></td>'  
    		                      }								
    							trTags = trTags + '<tr>' +
    					                          '<td>'+ response["data"]["networkcard"][i]["device"] +'</td>' +
    					                          '<td>'+ response["data"]["networkcard"][i]["macaddress"]+'</td>' +	
    						                      '<td>'+ response["data"]["networkcard"][i]["ip"] +'</td>' +
    						                      '<td>'+ response["data"]["networkcard"][i]["module"]+'</td>' +			
    						                      '<td>'+ response["data"]["networkcard"][i]["mtu"]+'</td>' +
    						                       status +
    					                        '</tr>';
    						};              			
    	        			netcardLiTags = '<li>' +
    						  '<div class="block">' +
    							'<div class="tags">' +
    							  '<a href="" class="tag">' +
    								'<span>网卡信息</span>' +
    							  '</a>' +
    							'</div>' +
    							'<div class="block_content">' +
    			                    '<table class="table table-striped">' +		                
    			                      '<tbody>' +
    			                        '<tr>' +
    			                          '<td>Name</td>' +
    			                          '<td>MAC</td>' +	
    				                      '<td>IPV4</td>' +
    				                      '<td>Speed</td>' +			
    				                      '<td>MTU</td>' +				
    				                      '<td>Status</td>' +			                        	
    			                        '</tr>' + trTags +		                        
    			                      '</tbody>' +
    			                    '</table>' +							
    							'</div>' +
    						  '</div>' +
    						'</li>';               			
    						
    	        		}
    	        		if (Object.keys(response["data"]["ram"]).length > 0){
    	        			var trTags = '';
    						for (var i=0; i <response["data"]["ram"].length; i++){
    		                      if (response["data"]["ram"][i]["device_status"]>0){
    		                    	  status = '<td><span class="label label-success">on</span></td>' 
    		                      }else{
    		                    	  status = '<td><span class="label label-danger">off</span></td>'  
    		                      }								
    							trTags = trTags + '<tr>' +
    					                          '<td>'+ response["data"]["ram"][i]["device_model"] +'</td>' +
    					                          '<td>'+ response["data"]["ram"][i]["device_volume"]+'</td>' +	
    						                      '<td>'+ response["data"]["ram"][i]["device_brand"] +'</td>' +
    						                      '<td>'+ response["data"]["ram"][i]["device_slot"]+'</td>' +			
    						                       status +
    					                        '</tr>';
    						};              			
    	        			ramLiTags = '<li>' +
    									  '<div class="block">' +
    										'<div class="tags">' +
    										  '<a href="" class="tag">' +
    											'<span>内存明细</span>' +
    										  '</a>' +
    										'</div>' +
    										'<div class="block_content">' +
    						                    '<table class="table table-striped">' +		                
    						                      '<tbody>' +
    						                        '<tr>' +
    						                          '<td>内存型号</td>' +
    						                          '<td>内存容量(GB)</td>' +	
    							                      '<td>生产商</td>' +
    							                      '<td>Slot</td>' +					
    							                      '<td>Status</td>' +			                        	
    						                        '</tr>' + trTags +		                        
    						                      '</tbody>' +
    						                    '</table>' +							
    										'</div>' +
    									  '</div>' +
    									'</li>';               			
    						
    	        		}   
    	        		if (Object.keys(response["data"]["disk"]).length > 0){
    	        			var trTags = '';
    						for (var i=0; i <response["data"]["disk"].length; i++){
    		                      if (response["data"]["disk"][i]["device_status"]>0){
    		                    	  status = '<td><span class="label label-success">on</span></td>' 
    		                      }else{
    		                    	  status = '<td><span class="label label-danger">off</span></td>'  
    		                      }								
    							trTags = trTags + '<tr>' +
    					                          '<td>'+ response["data"]["disk"][i]["device_model"] +'</td>' +
    					                          '<td>'+ response["data"]["disk"][i]["device_volume"]+'</td>' +	
    					                          '<td>'+ response["data"]["disk"][i]["device_serial"] +'</td>' +
    						                      '<td>'+ response["data"]["disk"][i]["device_brand"] +'</td>' +
    						                      '<td>'+ response["data"]["disk"][i]["device_slot"]+'</td>' +			
    						                       status +
    					                        '</tr>';
    						};              			
    	        			diskLiTags = '<li>' +
    									  '<div class="block">' +
    										'<div class="tags">' +
    										  '<a href="" class="tag">' +
    											'<span>硬盘明细</span>' +
    										  '</a>' +
    										'</div>' +
    										'<div class="block_content">' +
    						                    '<table class="table table-striped">' +		                
    						                      '<tbody>' +
    						                        '<tr>' +
    						                          '<td>硬盘型号</td>' +
    						                          '<td>硬盘容量</td>' +	
    						                          '<td>序列号</td>' +	
    							                      '<td>生产商</td>' +
    							                      '<td>Slot</td>' +					
    							                      '<td>Status</td>' +			                        	
    						                        '</tr>' + trTags +		                        
    						                      '</tbody>' +
    						                    '</table>' +							
    										'</div>' +
    									  '</div>' +
    									'</li>';               			
    						
    	        		}            		
    	        		$("#assets_info").html(ulTag + baseLiTags + serverLiTags + netcardLiTags + ramLiTags + diskLiTags + '</ul>');	
    	        	}
    	        }  
    		});    	
    		$(this).attr('disabled',false);
    })     

    $("#taggroupsubmit").on('click', function() {
    	var vIds = $(this).val();
    	var vServer = $('[name="doublebox"]').val()
    	if (vServer){
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
				contentType : "application/json", 
				dataType : "json", 	            
	            url:"/api/assets/tags/"+vIds+'/',  
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
    
});
