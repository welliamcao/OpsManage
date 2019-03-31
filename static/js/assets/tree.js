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

function draw_cpu_line(dataList){
	$("#draw_line_cpu").empty()
	$("#draw_line_cpu").length && (Morris.Line({
        element: "draw_line_cpu",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_taffic_line(dataList){
	$("#draw_line_taffic").empty()
	$("#draw_line_taffic").length && (Morris.Area(
		{
			parseTime: false,
	        element: "draw_line_taffic",
	        data: dataList,
	        xkey: "dtime",
	        ykeys: ["in", "out"],
	        lineColors: ["#26B99A", "#34495E"],
	        labels: ["in", "out"],
	        pointSize: 2,
	        hideHover: "auto",
	        resize: !0
	    }
    ), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_disk_line(dataList){
	$("#draw_line_disk").empty()
	$("#draw_line_disk").length && (Morris.Area(
		{
			parseTime: false,
	        element: "draw_line_disk",
	        data: dataList,
	        xkey: "dtime",
	        ykeys: ["read", "write"],
	        lineColors: ["#26B99A", "#34495E"],
	        labels: ["in", "out"],
	        pointSize: 2,
	        hideHover: "auto",
	        resize: !0
	    }
    ), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_mem_line(dataList){
	$("#draw_line_mem").empty()
	$("#draw_line_mem").length && (Morris.Area({
        element: "draw_line_mem",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function customMenu(node) {
      var items = {
              "new":{  
                  "label":"添加资产",  
                  "icon": "glyphicon glyphicon-plus",
                  "action":function(data){
                  	var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
//						$.alert({
//						    title: 'Alert!',
//						    content: '功能暂未开放',
//						});                  	
					    inst.create_node(obj, {}, "last", function (new_node) {
						try {
							new_node.text="新建设备";
							new_node.icon =  "fa fa-circle-o"
							inst.edit(new_node);
						} catch (ex) {
							setTimeout(function () { inst.edit(new_node); },0);
						}
					});
                  }  
              },
              "modf":{
              		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "修改名称",
					"shortcut_label"	: 'F2',
					"icon"				: "glyphicon glyphicon-leaf",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						inst.edit(obj)
//						console.log($(this.rename(obj))
//						$.alert({
//						    title: 'Alert!',
//						    content: '功能暂未开放',
//						});
					}
              },
              "view":{
              		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "资产明细",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-search-plus",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewAssets(obj)
					}
              },
              "tags":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "标签管理",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-bookmark",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewTags(obj)
					}
            },              
              "monitor":{
            		"separator_before"	: false,
					"separator_after"	: false,
					"_disabled"			: false, 
					"label"				: "监控信息",
					"shortcut_label"	: 'F2',
					"icon"				: "fa fa-bar-chart",
					"action"			: function (data) {
						var inst = $.jstree.reference(data.reference),
						obj = inst.get_node(data.reference);
						viewMonitor(obj)				
					}
            }, 
            "webssh":{
        		"separator_before"	: false,
				"separator_after"	: false,
				"_disabled"			: false, 
				"label"				: "打开终端",
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
					openTerminal(obj,parentsName)				
				}
        }            
//              "del":{
//              	"separator_before"	: false,
//					"icon"				: false,
//					"separator_after"	: false,
//					"_disabled"			: false, //(this.check("delete_node", data.reference, this.get_parent(data.reference), "")),
//					"label"				: "删除资产",
//					"icon"				:"glyphicon glyphicon-remove",
//					"action"			: function (data) {
//						var inst = $.jstree.reference(data.reference),
//							obj = inst.get_node(data.reference);
//						if(inst.is_selected(obj)) {
//							inst.delete_node(inst.get_selected());
//						}
//						else {
//							inst.delete_node(obj);
//						}
//					}
//              }
	  }
      if(node["id"]>10000 && node["id"] <= 20000){
    		try {    	  
	    	  delete items.view
	    	  delete items.monitor
	    	  delete items.tags
	    	  delete items.webssh
    		}
    		catch(err) {
    			console.log(err)
    		}     	  
      }else if(node["id"]>30000){
	    	try {    	  
	    	  delete items.new 
	    	  delete items.modf 
			}
			catch(err) {
				console.log(err)
			}     	  
      }else if(node["id"]>20000 && node["id"]<30000){
  		try {
	      	  delete items.new
	    	  delete items.view
	    	  delete items.monitor
	    	  delete items.tags
	    	  delete items.webssh
		}
		catch(err) {
			console.log(err)
		} 
      }
      return items
}


var serverList = []
function viewAssets(obj){
	if (obj["id"] > 30000){
		var aid = obj["id"] - 30000
    	$.ajax({  
            cache: true,  
            type: "get",    
            async: false,
            url:"/assets/manage/?id=" + aid + "&model=info",  
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
            		var divHtml = '<div class="col-md-12 col-sm-12 col-xs-12" '+ obj["id"] +'>' +
	                '<div class="x_panel">' +
	                  '<div class="x_title">' +
	                    '<h2><i class="fa fa-bars"></i>资产明细    <code>'+ obj["text"] +'</code><small>Assets Info</small></h2>' +
	                    '<div class="clearfix"></div>' +
	                  '</div>' +
	                  '<div class="x_content">' +	
	                    '<div class="col-md-4 col-sm-4 col-xs-12">' +
	                        '<p class="text-left">资产标签</p>'+
		                    '<canvas width="300" height="300" id="myCanvas'+ obj["id"] + '">' +
			                    '<ul>' + tagliTags +
			                    '</ul>' +
		                   '</canvas>' +
	                    '</div>' + 
	                    '<div class="col-md-8 col-sm-8 col-xs-12">' + 
		                    '<div class="" role="tabpanel" data-example-id="togglable-tabs">' +
		                      '<ul id="myTab1" class="nav nav-tabs bar_tabs right" role="tablist">' +
		                        '<li role="presentation" class=""><a href="#tab_content44'+ obj["id"] + '" role="tab" id="profile-tab4" data-toggle="tab" aria-controls="profile" aria-expanded="false">内存信息</a>' +
		                        '</li>' +	
		                        '<li role="presentation" class=""><a href="#tab_content55'+ obj["id"] + '" role="tab" id="profile-tab5" data-toggle="tab" aria-controls="profile" aria-expanded="false">硬盘信息</a>' +
		                        '</li>' +	
		                        '<li role="presentation" class=""><a href="#tab_content33'+ obj["id"] + '" role="tab" id="profile-tab3" data-toggle="tab" aria-controls="profile" aria-expanded="false">网卡信息</a>' +
		                        '</li>' +		                        
		                        '<li role="presentation" class=""><a href="#tab_content22'+ obj["id"] + '" role="tab" id="profile-tab2" data-toggle="tab" aria-controls="profile" aria-expanded="false">硬件信息</a>' +
		                        '</li>' +	                        
		                        '<li role="presentation" class="active"><a href="#tab_content11'+ obj["id"] + '" id="home-tabb" role="tab1" data-toggle="tab" aria-controls="home" aria-expanded="true">基础信息</a>' +
		                        '</li>' +	
	                        
		                      '</ul>' +
		                      '<div id="myTabContent2" class="tab-content">' +
		                        '<div role="tabpanel" class="tab-pane fade active in" id="tab_content11'+ obj["id"] +'" aria-labelledby="home-tab">' + baseLiTags +
		                        '</div>' +
		                        '<div role="tabpanel" class="tab-pane fade" id="tab_content22'+ obj["id"] + '" aria-labelledby="profile-tab">' + serverLiTags +
		                        '</div>' +
		                        '<div role="tabpanel" class="tab-pane fade" id="tab_content33'+ obj["id"] + '" aria-labelledby="profile-tab">' + netcardLiTags +
		                        '</div>' +
		                        '<div role="tabpanel" class="tab-pane fade" id="tab_content44'+ obj["id"] + '" aria-labelledby="profile-tab">' + ramLiTags +
		                        '</div>' +
		                        '<div role="tabpanel" class="tab-pane fade" id="tab_content55'+ obj["id"] + '" aria-labelledby="profile-tab">' + diskLiTags +
		                        '</div>' +									
		                      '</div>' +
	                      '</div>' +
	                    '</div>' +					
	                  '</div>' +
	                '</div>' +
	              '</div>'   
	             var vid = "#assetsInfo"+ obj["id"]   
	             var index = $.inArray(vid, serverList)
	             if (index>=0){
	            	 return false
	             }else{
	            	 $("#assets_info").prepend(divHtml);	
	            	 serverList.push(vid)
	             } 
            		   if( ! $('#myCanvas' + obj["id"]).tagcanvas({
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
	}else{
		$.alert({
		    title: 'Alert!',
		    content: '暂无更多信息',
		});		
	}
}


function getDateTime(seconds,fmt){
    var nowDate = new Date(new Date().getTime() - 1 * seconds * 1000);   
    var year = nowDate.getFullYear();  
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;  
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();  
    var hour = nowDate.getHours()< 10 ? "0" + nowDate.getHours() : nowDate.getHours();  
    var minute = nowDate.getMinutes()< 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();  
    var second = nowDate.getSeconds()< 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds(); 
	switch (fmt)
	{
		case 'yyyy-MM-dd':
			return year + "-" + month + "-" + date; 
		case 'yyyy/MM/dd HH:mm:SS':
			return year + "/" + month + "/" + date+" "+hour+":"+minute+":"+second;  
		case 'yyyyMMddHHmm':
			return year.toString() +  month.toString()  + date.toString() + hour.toString() +minute.toString() 
		case 'yyyy-MM-dd HH:mm':
			return year + "-" + month + "-" + date+" "+hour+":"+minute 
		case 'yyyy-MM-dd HH:mm:SS':
			return year + "-" + month + "-" + date+" "+hour+":"+minute+":"+second;  			            	
	}    
    
}

function draw_monitor_line(key,id,startTime,endtime){
	$.ajax({  
        cache: true,  
        type: "get",  
        url:'/api/monitor/assets/'+ id +'/?type='+key+'&startTime='+startTime+'&endtime=' + endtime,
        success: function(data) {  
        	switch (key)
        	{
        		case 'cpu':
        			draw_cpu_line(data)
        			break;
        		case 'mem':
        			draw_mem_line(data)
        			break; 
        		case 'disk':
        			draw_disk_line(data) 
        			break;
        		case 'taffic':
        			draw_taffic_line(data) 
        			break;
        	}         	
        	
        }  
	}); 
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


function viewMonitor(obj){
	var startTime = getDateTime(1800,'yyyyMMddHHmm') 
	var endtime = getDateTime(1,'yyyyMMddHHmm') 
	if (obj["id"] > 30000){
		var aid = obj["id"] - 30000	
		draw_monitor_line('cpu',aid,startTime,endtime)
		draw_monitor_line('mem',aid,startTime,endtime)
		draw_monitor_line('disk',aid,startTime,endtime)
		draw_monitor_line('taffic',aid,startTime,endtime)
		$("button[name^='monitor_']").val(aid).attr("disabled",false) 
    	$('.bs-example-modal-lg').modal({backdrop:"static",show:true});
	}
}


function viewTags(obj){
	if (obj["id"] > 30000){
		var aid = obj["id"] - 30000	
    	$("#myModalLabel").html('<h4 class="modal-title" id="myModalLabel"><code>'+ obj["text"] +'</code>标签分类</h4>')
    	$('select[name="doublebox"]').empty();
		$('#taggroupsubmit').val(aid)
    	var data = getAssetsTags(aid)
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
}

function openTerminal(obj,parentsName){
	if (obj["id"] > 30000){
		var aid = obj["id"] - 30000	
		$("#myWebsshModalLabel").html('<p class="text-blank"><code><i class="fa fa fa-terminal"></i></code>'+parentsName.replace(" ","_")+''+obj["text"]+ '</p>')
		$("#websshConnect").val(aid)	
		$('#webssh_tt').empty()
    	$('.bs-example-modal-webssh-info').modal({backdrop:"static",show:true}); 	
	}
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


$(document).ready(function () {
	
	drawTree('#projectTree',"/api/assets/tree/")
	
    $("#search-input").keyup(function () {
        var searchString = $(this).val();
        $('#projectTree').jstree('search', searchString);
    });
    
    $("#projectTree").click(function () {
        var position = 'last';
        var parent = $("#projectTree").jstree("get_selected");
        if (parent[0] > 20000 && parent[0] < 30000){
        	$("#projectTree").jstree("open_node", parent[0]);
            var serviceId = parent[0]-20000
        	$.ajax({  
                cache: true,  
                type: "GET",  
                url:"/api/assets/tree/service/" + serviceId + "/", 
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
					for (var i=0; i <response.length; i++){
						if (response[i]["status"]==0){
							var icon = "fa fa-desktop assets-online"
						}else{
							var icon = "fa fa-desktop assets-offline"
						}
						if (response[i]["mark"]){
							var text = response[i]["ip"]+' | '+response[i]["mark"]
						}else{
							var text = response[i]["ip"]
						}
                        var newNode = {
                                "id": response[i]["id"]+30000,
                                "text": text,
                                "icon": icon
                            }        						
						$('#projectTree').jstree('create_node', parent, newNode, position, false, false);	
					}
					$("#projectTree").jstree("open_node", parent);
	            } 
        	});                    
        }
    });
    
    $('#projectTree').on('rename_node.jstree', function (e, data) {
    	  //data.text is the new name:
    	  console.log(data.node);
    	  var vIds = data.node.id
    	  if (vIds > 20000 && vIds < 30000){
    		  	vIds = vIds - 20000
		    	$.ajax({  
		            cache: true,  
		            type: "PUT",  
		            url:"/api/service/" + vIds + '/',  
		            data:{"service_name":data.node.text},
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
		            }  
		    	});   		  
    	  }
    	  else if(vIds > 10000 && vIds < 20000  ){
    		  	vIds = vIds - 10000
		    	$.ajax({  
		            cache: true,  
		            type: "PUT",  
		            url:"/api/project/" + vIds + '/',  
		            data:{"project_name":data.node.text},
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
		            }  
		    	});     		  
    	  }
    }); 

    $('#projectTree').on('move_node.jstree', function (e, data) {
    	 if (data.node.id > 30000 && data.parent > 20000 && data.parent < 30000){
 		  	sIds = data.parent - 20000
 		  	aIds = data.node.id - 30000
	    	$.ajax({  
	            cache: true,  
	            type: "PUT",  
	            url:"/api/assets/tree/service/" + sIds + '/',  
	            data:{"aIds":aIds,"sIds":sIds},
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
	            }  
	    	}); 
    	 }
//    	 drawTree('#projectTree')
    }); 
    
    function disableButton(name){
  	  $("button[name^='monitor_']").each(function(){
		    if ($(this).attr("name") == name){
		    	$(this).attr("disabled",true);
		    }else{
		    	$(this).attr("disabled",false);
		    }
	  });
    }
    
    $("button[name='monitor_half_hour']").on("click", function(){
      	var vIds = $(this).val();
    	var startTime = getDateTime(1800,'yyyyMMddHHmm') 
    	var endtime = getDateTime(1,'yyyyMMddHHmm') 
    	draw_monitor_line('cpu',vIds,startTime,endtime)
    	draw_monitor_line('mem',vIds,startTime,endtime)
    	draw_monitor_line('disk',vIds,startTime,endtime)
    	draw_monitor_line('taffic',vIds,startTime,endtime) 
    	disableButton($(this).attr("name"))
      });     
    
    $("button[name='monitor_one_hour']").on("click", function(){
      	var vIds = $(this).val();
      	$(this).attr("disabled",true);
    	var startTime = getDateTime(3600,'yyyyMMddHHmm') 
    	var endtime = getDateTime(1,'yyyyMMddHHmm') 
    	draw_monitor_line('cpu',vIds,startTime,endtime)
    	draw_monitor_line('mem',vIds,startTime,endtime)
    	draw_monitor_line('disk',vIds,startTime,endtime)
    	draw_monitor_line('taffic',vIds,startTime,endtime) 
    	disableButton($(this).attr("name"))
      });   
    
    $("button[name='monitor_six_hour']").on("click", function(){
      	var vIds = $(this).val();
      	$(this).attr("disabled",true);
    	var startTime = getDateTime(3600*6,'yyyyMMddHHmm') 
    	var endtime = getDateTime(1,'yyyyMMddHHmm') 
    	draw_monitor_line('cpu',vIds,startTime,endtime)
    	draw_monitor_line('mem',vIds,startTime,endtime)
    	draw_monitor_line('disk',vIds,startTime,endtime)
    	draw_monitor_line('taffic',vIds,startTime,endtime) 
    	disableButton($(this).attr("name"))
      });     
    
    $("button[name='monitor_one_day']").on("click", function(){
      	var vIds = $(this).val();
      	$(this).attr("disabled",true);
    	var startTime = getDateTime(3600*24,'yyyyMMddHHmm') 
    	var endtime = getDateTime(1,'yyyyMMddHHmm') 
    	draw_monitor_line('cpu',vIds,startTime,endtime)
    	draw_monitor_line('mem',vIds,startTime,endtime)
    	draw_monitor_line('disk',vIds,startTime,endtime)
    	draw_monitor_line('taffic',vIds,startTime,endtime) 
    	disableButton($(this).attr("name"))
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
    
});








