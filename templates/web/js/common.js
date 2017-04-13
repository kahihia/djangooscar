$(document).ready(function(){
	$('.check_wrap input').iCheck({
		checkboxClass: 'icheckbox_minimal', 
		radioClass: 'iradio_minimal',
		increaseArea: '20%' 
	});

		$('.small_check_wrap input').iCheck({
		checkboxClass: 'icheckbox_minimal_small', 
		radioClass: 'iradio_minimal',
		increaseArea: '20%' 
	});
});

$(window).load(function(){
	$(".sgnb_show>a").on("click",function(){
		$(this).next(".s_gnb_wrap").fadeToggle(250);
		return false;
	});

	$(".view_wrap .thumbnail li").on("click",function(){
		var a = $(this).find("img").attr("src");
		$(".big_img").find("img").attr("src",a);
		return false;
	});

	$(".language>a").on("click",function(){
		$(".other_site").stop().slideDown("fast");
		return false;
	});
	$(".language").on("mouseleave",function(){
		$(".other_site").stop().slideUp("fast");
	});


});