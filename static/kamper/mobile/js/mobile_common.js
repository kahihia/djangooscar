//$(document).ready(function(){
//	$('.checkbox_wrap input').iCheck({
//		checkboxClass: 'icheckbox_minimal',
//		radioClass: 'iradio_minimal',
//		increaseArea: '20%'
//	});
//
//		$('.small_check_wrap input').iCheck({
//		checkboxClass: 'icheckbox_minimal_small',
//		radioClass: 'iradio_minimal',
//		increaseArea: '20%'
//	});
//});

$(window).load(function(){
	$(".language>a").on("click",function(){
		$(".other_site").stop().slideToggle(200);
		return false;
	});

	$(".navi_menu>a").on("click",function(){
		$(this).next(".navi_2dep").stop().slideToggle(200);
		return false;
	});

	$(".gnb_open").on("click",function(){
		var win_h = $(window).height();
		var doc_h = $(document).height();

		if (win_h > doc_h){
			$('.gnb_wrap').css({"height":win_h-57+"px"});
		} else {
			$('.gnb_wrap').css({"height":doc_h-57+"px"});
		}
		$(".gnb_bg").stop().fadeToggle(200);
		$(".gnb_wrap").stop().fadeToggle(200);
	});
	
	$(".view_rolling_li li").css({"display":"block"});
	$(".view_rolling_li ul").carouFredSel({
		pagination:".view_paging",
		prev : ".view_rolling_prev",
		next : ".view_rolling_next",
		auto : false,
		responsive : true,
		swipe:{onTouch:true,onMouse:true},
		items:{height:"variable",visible:1},
		scroll: {
			timeoutDuration:3000,
			duration:500
				}
	});

	$(".sgnb_show>a").on("click",function(){
		$(".s_gnb").slideToggle(200);
		$(".sgnb_show").toggleClass("on");
		return false;
	});

	


});