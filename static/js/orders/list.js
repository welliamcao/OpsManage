function makeOrderLogsTableList(url){
    var columns = [		                   
                    {"data": "order"},
                    {"data": "operator"},
                    {"data": "operation_info"},
                    {"data": "audit_status"},
                    {"data": "execute_status"},
	                {"data": "operation_time"}			                			                
	               ]
    var columnDefs = [			                      
						{
							targets: [3],
							render: function(data, type, row, meta) {
						        return orderAuditStatusHtml[row.audit_status]
							},
						},
						{
							targets: [4],
							render: function(data, type, row, meta) {
						        return orderExecuteStatusHtml[row.execute_status]
							},
						}						
	    		      ]
    
    var buttons = [
			    					    
    ] 		    
    InitDataConfigTable('ordersLogs',url,buttons,columns,columnDefs);   		
}

function search_go() {
    var parameter = {};
    $("input[type='hidden'][name^='order_']").each(function () {
        var key = $(this).prop('name');
        var value = $(this).val();
        parameter[key] = value;    
    })

    var count = 0;
    for (var i in parameter) {
        count += i;
        break;
    }
    if (count == 0) {
        return false;
    }

    $.post('/api/orders/list/', parameter, function (result) {
        if (result.length > 0) {
/*                 	document.getElementById("div-search-result").style.display = ""; */
				 var table = $('#ordersLists').dataTable();
				 oSettings = table.fnSettings();
				 table.fnClearTable(this);
				 for (var i=0; i<result.length; i++)
				 {
				   table.oApi._fnAddData(oSettings, result[i]);
				 }
				 oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
				 table.fnDraw();                	               	
        }
        else{
        	//没有数据就清空
        	var table = $('#ordersLists').dataTable();
        	table.fnClearTable(this);
        }
    })
}

function changepage(pageindex) {
    curpage = pageindex;
    search_go();
}

function removeself(obj) {
    $(obj).parent().remove();
    changepage(1);
}

$(document).ready(function() {

	$("input[name='order_time']").daterangepicker({
        timePicker: !0,
        timePickerIncrement: 30,
        locale: {
            format: "YYYY-MM-DD HH:mm:ss"
        }
    })		

    $('#selExpired').change(function () {
        if ($('#selExpired').val() != "") {
            $("#hdnExpired").val($('#selExpired').val());
            var span = "<span class='tag' id='spanExpired'>" + $("#selExpired").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_expire' type='hidden' value='"
            + $('#selExpired').val() + "' /></span> &nbsp;";
            if ($("#spanExpired").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanExpired").html($("#selExpired").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_expire' type='hidden' value='"
                 + $('#selExpired').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })     
    
    $('#selOrderTime').change(function () {
        if ($('#selOrderTime').val() != "") {
            var span = "<span class='tag' id='spanOrderTime'>" + $("#selOrderTime").val()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x</a><input name='order_time' type='hidden' value='"
            + $('#selOrderTime').val() + "'/></span> &nbsp;";
            if ($("#spanOrderTime").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanOrderTime").html($("#selOrderTime").val()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x</a><input name='order_time' type='hidden' value='"
                 + $('#selOrderTime').val() + "'/></span> &nbsp;");
            }
            changepage(1);
        }
    })      
    
    $('#selOrderType').change(function () {
        if ($('#selOrderType').val() != "") {
            $("#hdnOrderType").val($('#selOrderType').val());
            var span = "<span class='tag' id='spanOrderType'>" + $("#selOrderType").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_type' type='hidden' value='"
            + $('#selOrderType').val() + "' /></span> &nbsp;";
            if ($("#spanOrderType").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanOrderType").html($("#selOrderType").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_type' type='hidden' value='"
                 + $('#selOrderType').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })  
	
    $('#selExecute').change(function () {
        if ($('#selExecute').val() != "") {
            $("#hdnExecute").val($('#selExecute').val());
            var span = "<span class='tag' id='spanExecute'>" + $("#selExecute").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_execute_status' type='hidden' value='"
            + $('#selExecute').val() + "' /></span> &nbsp;";
            if ($("#spanExecute").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanExecute").html($("#selExecute").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_execute_status' type='hidden' value='"
                 + $('#selExecute').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })   

    $('#selAudit').change(function () {
        if ($('#selAudit').val() != "") {
            $("#hdnAudit").val($('#selAudit').val());
            var span = "<span class='tag' id='spanAudit'>" + $("#selAudit").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_audit_status' type='hidden' value='"
            + $('#selAudit').val() + "' /></span> &nbsp;";
            if ($("#spanAudit").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanAudit").html($("#selAudit").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_audit_status' type='hidden' value='"
                 + $('#selAudit').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })     
    
    $('#selAuditUser').change(function () {
        if ($('#selAuditUser').val() != "") {
            $("#hdnAuditUser").val($('#selAuditUser').val());
            var span = "<span class='tag' id='spanAuditUser'>" + $("#selAuditUser").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_user' type='hidden' value='"
            + $('#selAuditUser').val() + "' /></span> &nbsp;";
            if ($("#spanAuditUser").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanAuditUser").html($("#selAuditUser").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_user' type='hidden' value='"
                 + $('#selAuditUser').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })      
    
    $('#selExecuteUser').change(function () {
        if ($('#selExecuteUser').val() != "") {
            $("#hdnExecuteUser").val($('#selExecuteUser').val());
            var span = "<span class='tag' id='spanExecuteUser'>" + $("#selExecuteUser").find("option:selected").text()
            + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_executor' type='hidden' value='"
            + $('#selExecuteUser').val() + "' /></span> &nbsp;";
            if ($("#spanExecuteUser").length == 0) {
            	$("#divSelectedType").show();
                $('#divSelectedType').append(span);
            }
            else {
                $("#spanExecuteUser").html($("#selExecuteUser").find("option:selected").text()
                 + "&nbsp;&nbsp;<a  title='Removing tag' onclick='removeself(this)'>x<input name='order_executor' type='hidden' value='"
                 + $('#selExecuteUser').val() + "' /></span> &nbsp;");
            }
            changepage(1);
        }
    })     
    
	$("button[name='noticeonfig']").on("click", function(){
		var vIds = $(this).val();
		if (vIds > 0){
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/'+vIds+'/', //请求地址
				type:"PUT",  //提交类似
				data:{
					"order_type":$('#order_type option:selected').val(),
					"mode":$('#mode option:selected').val(),
					"number":$("#number").val()
				}, //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '修改成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
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
		}else{
			$.ajax({
				dataType: "JSON",
				url:'/api/orders/notice/', //请求地址
				type:"POST",  //提交类似
				data:$("#order_config").serialize(), //提交参数
				success:function(response){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '添加成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                });   
	            	RefreshConfigTable('configList', '/api/orders/notice/')
				
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
		}
	})
	
	function makeConfigList(){
	    var columns = [
	                   	{"data": "id","className": "text-center",},
	                    {"data": "order_type","className": "text-center",},	
	                    {"data": "mode","className": "text-center",},
/*	                    {"data": "number","className": "text-center",},*/
		               ]
	    var columnDefs = [		
	   	    		    {
	    	    				targets: [1],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	    					return orderTypeHtml[row.order_type]
	    	    				},
	    	    				"className": "text-center",
   	    		        },	    
   	    		        {
    	    				targets: [2],
    	    				render: function(data, type, row, meta) {		    	    					
    	    					return '<strong>'+orderMode[row.mode]+'</strong>'
    	    				},
    	    				"className": "text-center",
	    		        },  	    		        
   	    		        {
	    	    				targets: [3],
	    	    				render: function(data, type, row, meta) {		    	    					
	    	                        return '<div class="btn-group  btn-group-xs">' +	
		    	                           '<button type="button" name="btn-config-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
		    	                           '</button>' +                 				                            		                            			                          
		    	                           '<button type="button" name="btn-config-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
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
		InitDataConfigTable('configList',"/api/orders/notice/",buttons,columns,columnDefs)
	}	  
	makeConfigList()	
	
    $('#configList tbody').on('click',"button[name='btn-config-edit']", function(){
    	var vIds = $(this).val();    	
		$.ajax({
			dataType: "JSON",
			url:'/api/orders/notice/'+vIds+'/', //请求地址
			type:"GET",  //提交类似
			success:function(response){
				DynamicSelect("order_type",response["order_type"])	
				$("#order_type").prop('disabled', true);
				DynamicSelect("grant_group",response["grant_group"])	
				DynamicSelect("mode",response["mode"])
				$("#number").val(response["number"])
				$('.selectpicker').selectpicker('refresh');	
				$("button[name='noticeonfig']").val(vIds).text("修改")
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

    $('#configList tbody').on('click',"button[name='btn-config-delete']", function(){
    	var vIds = $(this).val();
    	var td = $(this).parent().parent().parent().find("td")
    	var name = td.eq(1).text(); 
    	var mode = td.eq(2).text();
		$.confirm({
		    title: '删除确认',
		    content: "确认删除:【"+ name +"】使用<strong>"+mode+"</strong>发送通知方式？",
		    type: 'red',
		    buttons: {
		        删除: function () {
		    	$.ajax({  
		            type: "DELETE",  
		            url:'/api/orders/notice/'+vIds+'/',  
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
		            	RefreshConfigTable('configList', '/api/orders/notice/')
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		}) 	
    })  	
	
	
	var userList = requests("get","/api/account/user/")
	for (var i=0; i <userList.length; i++){
		userInfo[userList[i]["id"]] = userList[i]
	}
	
	if($("#selAuditUser").length){
		makeUserSelect("selAuditUser", userList)
	}
	
	if($("#selExecuteUser").length){
		makeUserSelect("selExecuteUser", userList)
	}	
	
    if ($("#ordersLists").length) {
    	
        $("button[name^='orders_page_']").on("click", function(){
          	var url = $(this).val();
          	$(this).attr("disabled",true);
          	if (url.length){
          		RefreshTable('ordersLists', url, 'orders');
          	}      	
        	$(this).attr('disabled',false);
          }); 
    	
    	var currentUser = $("#currentUser").val()
    	
    	function makeOrderTableList(){
		    var columns = [
		                   	{
		                   		"className":      'details-control',
			                    "orderable":      false,
			                    "data":           null,
			                    "defaultContent": ''
			                },		                   
		                    {"data": "id"},
		                    {"data": "order_type"},
		                    {"data": "order_user"},
			                {"data": "order_subject"},
			                {"data": "order_executor"},	
			                {"data": "create_time"},	
			                {"data": "order_execute_status","className": "text-center",},
			                {"data": "order_audit_status","className": "text-center",},	
			                {"data": "expire","className": "text-center",},	
			                {"data": "end_time"},			                			                
			               ]
		    var columnDefs = [			                      
								{
									targets: [2],
									render: function(data, type, row, meta) {
										return orderTypeHtml[row.order_type]
									},
								},
								{
									targets: [3],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_user]["name"]
									},
								},
								{
									targets: [5],
									render: function(data, type, row, meta) {
								        return userInfo[row.order_executor]["name"]
									},
								},	
								{
									targets: [7],
									render: function(data, type, row, meta) {
								        return orderExecuteStatusHtml[row.order_execute_status]
									},
								},									
								{
									targets: [8],
									render: function(data, type, row, meta) {
								        return orderAuditStatusHtml[row.order_audit_status]
									},
								},		
								{
									targets: [9],
									render: function(data, type, row, meta) {
										switch(row.expire){
										case 1:
											return '<span class="label label-success">未过期</span>'
										case 2:
											return '<span class="label label-warning">未到期</span>'											
										default:
											return '<span class="label label-danger">已过期</span>'
										}
									},
								},								
	    	    		        {
		    	    				targets: [11],
		    	    				render: function(data, type, row, meta) {	
		    	    					if (currentUser==row.order_executor || userInfo[currentUser]["is_superuser"]){
		    	    						/*如果是工单完成人或者超级管理员授权*/
		    	    						var grant = '<button type="button" name="btn-order-grant" value="'+ row.id + ':' + row.order_audit_status  +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-check" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var grant = ''
		    	    					}		    	    					
		    	    					if (userInfo[currentUser]["is_superuser"]){
		    	    						/*如果是运维服务工单已授权，*/
		    	    						var edit = '<button type="button" name="btn-order-edit" value="'+ row.id + ':' + row.order_execute_status  +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span></button>'
		    	    					}else{
		    	    						var edit = ''
		    	    					}
		    	    					/*----------*/
		    	    					switch(row.order_type)
		    	    					{
		    	    					case 0:
		    	    						var url = '/order/sql/handle/?id='+row.id
		    	    					  break;
		    	    					case 2:
		    	    						var url = '/order/fileupload/handle/?id='+row.id
		    	    					  break;
		    	    					case 3:
		    	    						var url = '/order/filedownload/handle/?id='+row.id
		    	    					  break;		    	    						
		    	    					default:
		    	    						var url = '/order/service/handle/?id='+row.id
		    	    					}
		    	                        return '<div class="btn-group  btn-group-sm">' +	
			    	                           '<button type="button" name="btn-order-run" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><a href="'+url+'"><span class="glyphicon glyphicon-play-circle" aria-hidden="true"></span></a>' +	
			    	                           '</button>' + grant + edit + 	
			    	                           '<button type="button" name="btn-order-log" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-log"><span class="fa fa-search-plus" aria-hidden="true"></span></button>'
			    	                           '</div>';
		    	    				},
		    	    				"className": "text-center",
	    	    		        },
	    	    		      ]
		    
		    var buttons = [
						    {
						        text: '<span class="fa fa-cogs"></span>',
						        className: "btn-sm",
						        action: function ( e, dt, node, config ) {        	
		    	                    if($('#noticeConfigDiv').is(':hidden')){
		    	                    	$('#noticeConfigDiv').show();
		    	                    }
		    	                    else{
		    	                    	$('#noticeConfigDiv').hide();
		    	                    } 						        	
						        }
						    },		                   
		                   {
					        text: '<span class="fa fa-cubes"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) { 
					        	window.open('/order/apply/')
					        }
					    },
					    {
					        text: '<span class="fa fa-cloud-upload"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },	
					    {
					        text: '<span class="fa fa-cloud-download"></span>',
					        className: "btn-sm",
					        action: function ( e, dt, node, config ) {        	
					        	window.open('/order/apply/')
					        }
					    },						    
					    
		    ] 		    
		    InitDataTable('ordersLists','/api/orders/list/',buttons,columns,columnDefs,'orders');   		
    	}
    	
    	makeOrderTableList()
    	
    	var table = $('#ordersLists').DataTable();
    	
    	$('#ordersLists tbody').on('click', 'td.details-control', function () {
	    	var dataList = [];
	        var tr = $(this).closest('tr');
	        var row = table.row( tr );	        
	        aId = row.data()["id"];
	        order_type = row.data()["order_type"]
	        $.ajax({
//	            url : "/order/info/?type="+ orderTypeJson[order_type] +"&&id="+aId,
	        	url: "/api/orders/"+ aId +"/",
	            type : "get",
	            async : false,
	            success : function(result) {
	            	dataList = result;
	            }
	        });	        
	        if ( row.child.isShown() ) {
	            row.child.hide();
	            tr.removeClass('shown');
	        }
	        else {
	            row.child( orderInfoFormat(dataList) ).show();
	            tr.addClass('shown');
	        }
	        switch(order_type)
	        {
	        case 0:
		        $('#tooltips-sql-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_sql"].replace(/;/g, ";<br>") 
		        }); 
		        $('#tooltips-err-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_err"].replace(/;/g, ";<br>") 
		        });
	          break;
	        case 1:
		        $('#tooltips-order_content-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_content"]
		        });	
	          break;	          
	        case 2:
	        	var server = ''
	        	for (var i=0; i <dataList["detail"]["server"].length; i++){
	        		server += dataList["detail"]["server"][i] + ';'
	        	}
		        $('#tooltips-order_content-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: dataList["detail"]["order_content"]
		        });	
		        $('#tooltips-order_server-'+aId).pt({
		            position: 'r', // 默认属性值
		            align: 'c',	   // 默认属性值
		            height: 'auto',
		            width: 'auto',
		            content: server.replace(/;/g, "<br>") 
		        });	        
	          break;
	        case 3:
	        	var server = ''
		        	for (var i=0; i <dataList["detail"]["server"].length; i++){
		        		server += dataList["detail"]["server"][i] + ';'
		        	}
			        $('#tooltips-order_content-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: dataList["detail"]["order_content"]
			        });	
			        $('#tooltips-order_server-'+aId).pt({
			            position: 'r', // 默认属性值
			            align: 'c',	   // 默认属性值
			            height: 'auto',
			            width: 'auto',
			            content: server.replace(/;/g, "<br>") 
			        });	 	        	
	          break;
	        default:
	          break;
	        }         
	    });	
    	 
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-grant"]',function(){
    		var vIds = $(this).val().split(":");
    		let orderInfo = $(this).parent().parent().parent().find("td")
    		let username =  orderInfo.eq(3).text()
    		let order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'blue',
    	        title: '修改<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单审核状态?',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
				            '<div class="form-group">' +
				              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">工单状态<span class="required">*</span>' +
				              '</label>' +
				              '<div class="col-md-6 col-sm-6 col-xs-12">' +
				              			makeOrderAuditStatusSelect(parseInt(vIds[1])) +
				              '</div>' +
				            '</div>' + 
					        '<div class="form-group">' +
					        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">审批建议: <span class="required">*</span>' +
					        '</label>' +
					        '<div class="col-md-6 col-sm-6 col-xs-12">' +
					          '<input type="text"  name="order_mark" class="form-control col-md-7 col-xs-12">' +
					        '</div>' +				            
				          '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                	var formData = {};	
    	            		var vipForm = this.$content.find('select,input');                	
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
    				            url:"/api/orders/" + vIds[0] + '/',  
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
    				                    text: '工单授权成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshTable('ordersLists','/api/orders/list/', 'orders')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	  
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-edit"]',function(){
    		var vIds = $(this).val().split(":");
    		let orderInfo = $(this).parent().parent().parent().find("td")
    		let username =  orderInfo.eq(3).text()
    		let order_subject = orderInfo.eq(4).text()
    	    $.confirm({
    	        icon: 'fa fa-check',
    	        type: 'blue',
    	        title: '修改<code>'+username+'</code>申请的<strong>《'+ order_subject  + '》</strong>工单进度?',
    	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
				            '<div class="form-group">' +
				              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">工单进度<span class="required">*</span>' +
				              '</label>' +
				              '<div class="col-md-6 col-sm-6 col-xs-12">' +
				              		 makeOrderExecuteStatusSelect(parseInt(vIds[1])) +
				              '</div>' +
				            '</div>' + 
					        '<div class="form-group">' +
					        '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">处理建议: <span class="required">*</span>' +
					        '</label>' +
					        '<div class="col-md-6 col-sm-6 col-xs-12">' +
					          '<input type="text"  name="order_mark"  class="form-control col-md-7 col-xs-12">' +
					        '</div>' +				            
				          '</form>',
    	        buttons: {
    	            '取消': function() {},
    	            '确认': {
    	                btnClass: 'btn-blue',
    	                action: function() {
    	                	var formData = {};	
    	            		var vipForm = this.$content.find('select,input');                	
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
    				            url:"/api/orders/" + vIds[0] + '/',  
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
    				                    text: '工单授权成功',
    				                    type: 'success',
    				                    styling: 'bootstrap3'
    				                }); 
    				            	/*RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))*/
    				            	RefreshTable('ordersLists','/api/orders/list/', 'orders')
    				            }  
    				    	});
    	                }
    	            }
    	        }
    	    });     		
    	});	 
    	
    	$('#ordersLists tbody').on('click','button[name="btn-order-log"]',function(){
    		var vIds = $(this).val();
    		orderInfo = $(this).parent().parent().parent().find("td")
    		order_subject = orderInfo.eq(4).text()
    		$("#orderLogModalLabel").text(order_subject)
    		if ($('#ordersLogs').hasClass('dataTable')) {
    			dttable = $('#ordersLogs').dataTable();
    			dttable.fnClearTable(); //清空table
    			dttable.fnDestroy(); //还原初始化datatable
    		}	    		
    		makeOrderLogsTableList("/api/orders/logs/"+ vIds +"/")
    	});    	
    	
	}
    
	
})