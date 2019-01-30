/**
 * jQuery带箭头提示框插件
 * email: tianshaojie@msn.com
 * date: 2013-01-15
 * version: 1.0.0
 */
(function($) {
	var max = Math.max,
		min = Math.min;
	$.pt = $.pureToolTips = function(options) {
		var opts = $.extend({
			target 		: null,		//目标元素，不能为空
			position 	: 't',		//提示框相对目标元素位置 t=top,b=bottom,r=right,l=left
			align		: 'c',		//提示框与目标元素的对齐方式，自动调节箭头显示位置，指向目标元素中间位置，c=center, t=top, b=bottom, l=left, r=right [postion=t|b时，align=l|r有效][position=t|b时，align=t|d有效]
			arrow		: true,		//是否显示箭头
			content 	: '',		//内容
			width 		: 200,		//宽度
			height 		: 'auto',	//高度
			autoClose 	: true,		//是否自动关闭
			time 		: 2000,		//自动关闭延时时长
			leaveClose 	: false,	//提示框失去焦点后关闭
			close 		: null		//关闭回调函数
		}, options || {}),

		$ao, $ai, w, h,
		$pt = $('.pt'),
		$target = $(opts.target),
		top = $target.offset().top,
		left = $target.offset().left,
		width = $target.outerWidth(),
		height = $target.outerHeight(),

		position = opts.position,
		align = opts.align,
		arrow = opts.arrow,

		constant = {b:'pt-up', t:'pt-down', r:'pt-left', l:'pt-right'}, //相对位置正好和箭头方向相反
		arrowClass = constant[position] || constant.t;

		//初始化元素，事件
		function init() {
			if(!opts.target) {
				return;
			}
			if(!$pt.length) {
				$pt = $('<div class="pt pt-down"><div class="cont"></div><b class="out"></b><b class="in"></b></div>').appendTo(document.body);
			}
			$pt.removeClass().addClass('pt ' + (arrow ? arrowClass : '')).find('.cont').html(opts.content).css({width:opts.width, height:opts.height});
			$ao = $pt.find('.out').toggle(arrow);
			$ai =  $pt.find('.in').toggle(arrow);
			w = $pt.outerWidth();
			h = $pt.outerHeight();
			arrow && autoAdjust();			//设置箭头自动居中
			$pt.css(setPos()).show();		//设置显示框位置和自动隐藏事件
			opts.leaveClose && leaveClose();//离开关闭
			opts.autoClose && !opts.leaveClose && autoClose(opts.timeout);	//默认自动关闭，优先离开关闭
			return $pt;
		}
		//计算提示框应该出现在目标元素位置
		function setPos() {
			var btw = arrow ? parseInt($ao.css('border-top-width'), 10) : 3,
				brw = arrow ? parseInt($ao.css('border-right-width'), 10) : 3,
				result = {};
			switch(align) {
				case 'c': break;
				case 't': result.top = top; break;
				case 'b': result.top = top + height - h; break;
				case 'l': result.left = left; break;
				case 'r': result.left = left + width - w; break;
			}
			switch(position) {
				case 't': result.top = top - h - brw; break;
				case 'b': result.top = top + height + brw; break;
				case 'l': result.left = left - w - btw; break;
				case 'r': result.left = left + width + btw; break;
			}
			result.top || (result.top = top + height/2 - h/2);
			result.left || (result.left = left + width/2 - w/2);
			return result;
		}

		//设置箭头自动居中
		function autoAdjust() {
			var aop, aip, bw, auto='auto';
			switch(position) {
				case't':
					bw = parseInt($ao.css('border-top-width'), 10);
					aop = {bottom:-bw, left:w/2-bw, top:auto, right:auto};
					alignLR();
					aip = {top:auto, left:aop.left+1, bottom:aop.bottom+1, right:auto};
					break;
				case'b':
					bw = parseInt($ao.css('border-bottom-width'), 10);
					aop = {top:-bw, left:w/2 - bw, right:auto, bottom:auto};
					alignLR();
					aip = {top:aop.top+1, left:aop.left+1, bottom:auto, right:auto};
					break;
				case'l':
					bw = parseInt($ao.css('border-left-width'), 10);
					aop = {top:h/2 - bw, right:-bw, left:auto, bottom:auto};
					alignTB();
					aip = {top:aop.top+1, right:aop.right+1, left:auto, bottom:auto};
					break;
				case'r':
					bw = parseInt($ao.css('border-right-width'), 10);
					aop = {top:h/2 - bw, left:-bw, right:auto, bottom:auto};
					alignTB();
					aip = {top:aop.top+1, left:aop.left+1, right:auto, bottom:auto};
					break;
			}
			//上下侧，左右对齐
			function alignLR() {
				if(align === 'l' && width/2 > bw && width/2 < w-bw) {
					aop.left = width/2-bw/2;
				} else if(align === 'r' && width/2 > bw && width/2 < w-bw) {
					aop.left = w-width/2-bw/2;
				}
			}
			//左右侧，上下对齐
			function alignTB() {
				if(align === 't' && height/2 > bw && height/2 < h-bw) {
					aop.top = height/2 - bw;
				} else if(align === 'b' && height/2 > bw && height/2 < h-bw) {
					aop.top = h - height/2 - bw;
				}
			}
			$ao.css(aop);
			$ai.css(aip);
		}
		//设置提示框自动关闭
		function autoClose() {
			window.ptt && clearTimeout(ptt);
			window.pta && clearTimeout(pta);
			window.pta = setTimeout(function() {
				$pt.hide();
				$.isFunction(opts.close) && opts.close();
			}, opts.time);
		}
		//设置提示框失去焦点关闭
		function leaveClose() {
			//先解绑再绑定，不然会形成事件链
			$pt.unbind('mouseleave').mouseleave(function(e) {
				$pt.hide();
				$.isFunction(opts.close) && opts.close();
			}).unbind('mouseenter').mouseenter(function() {
				window.ptt && clearTimeout(ptt);
			});
		}
		return init();
	};

	//扩展到包装集上
	$.fn.pt = $.fn.pureToolTips = function(options) {
		var opts = $.extend({
			leaveClose:true
		}, options || {});
		return this.each(function() {
			$(this).mouseenter(function() {
				window.ptt && clearTimeout(ptt);
				window.pta && clearTimeout(pta);
				opts.target = this;
				$.pt(opts);
			}).mouseleave(function() {
				window.ptt = setTimeout(function() {
					$('.pt').hide();
					$.isFunction(opts.close) && opts.close();
				}, 500);
			});
		});
	};
})(jQuery);