"use strict";
jQuery(document).on('ready', function() {
	/* MOBILE MENU*/
	function collapseMenu(){
		jQuery('.wt-navigation ul li.menu-item-has-children, .wt-navdashboard ul li.menu-item-has-children, .wt-navigation ul li.menu-item-has-mega-menu').prepend('<span class="wt-dropdowarrow"><i class="lnr lnr-chevron-right"></i></span>');
		jQuery('.wt-navigation ul li.menu-item-has-children span, .wt-navigation ul li.menu-item-has-mega-menu span').on('click', function() {
			jQuery(this).parent('li').toggleClass('wt-open');
			jQuery(this).next().next().slideToggle(300);
		});
		jQuery('.wt-navdashboard ul li.menu-item-has-children').on('click', function(){
			jQuery(this).toggleClass('wt-open');
			jQuery(this).find('.sub-menu').slideToggle(300);
		});
	}
	collapseMenu();
	
	/* PROGRESS BAR */
	if(jQuery('#wt-ourskill').length > 0){
		var _wt_ourskill = jQuery('#wt-ourskill');
		_wt_ourskill.appear(function () {
			jQuery('.skill-holder').each(function () {
				jQuery(this).find('.skill-bar').animate({
					width: jQuery(this).attr('data-percent')
				}, 2500);
			});
		});
	}
	
	/* Google Map */
	if(jQuery('#wt-locationmap').length > 0){
		var _wt_locationmap = jQuery('#wt-locationmap');
		_wt_locationmap.gmap3({
			marker: {
				address: '1600 Elizabeth St, Melbourne, Victoria, Australia',
				options: {
					title: 'Robert Frost Elementary School'
				}
			},
			map: {
				options: {
					zoom: 16,
					scrollwheel: false,
					disableDoubleClickZoom: true,
				}
			}
		});
	}
	/*OPEN CLOSE */
	jQuery('#wt-loginbtn, .wt-loginheader a').on('click', function(event){
		event.preventDefault();
		jQuery('.wt-loginarea .wt-loginformhold').slideToggle();
	});
	/*OPEN CLOSE */
	jQuery('.wt-dropdown').on('click', function(event){
		event.preventDefault();
		jQuery('.wt-radioholder').slideToggle();
	});
	/* BANNER VIDEO */
	jQuery("a[data-rel]").each(function () {
		jQuery(this).attr("rel", jQuery(this).data("rel"));
	});
	jQuery("a[data-rel^='prettyPhoto']").prettyPhoto({
		animation_speed: 'normal',
		theme: 'dark_square',
		slideshow: 3000,
		autoplay_slideshow: false,	
		social_tools: false
	});
	/* DROPDOWN RADIO */
	jQuery('input:radio[name="searchtype"]').on('change',
	    function(){
	        var _type = jQuery(this).data('title');
	        jQuery('.selected-search-type').html(_type);
	    }
    );
    /* COUNTER */
	try {
		var _wt_statistics = jQuery('#wt-statistics');
		_wt_statistics.appear(function () {
			var _wt_statistics = jQuery('.wt-statisticcontent h3');
			_wt_statistics.countTo({
				formatter: function (value, options) {
					return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
				}
			});
		});
	} catch (err) {}

	/* OUR PROFESSIONALS FILTERABLE*/
	var $container = jQuery('.wt-teamfilter');
	var $optionSets = jQuery('.option-set');
	var $optionLinks = $optionSets.find('a');
	function doIsotopeFilter() {
		if (jQuery().isotope) {
			var isotopeFilter = '';
			$optionLinks.each(function () {
				var selector = jQuery(this).attr('data-filter');
				var link = window.location.href;
				var firstIndex = link.indexOf('filter=');
				if (firstIndex > 0) {
					var id = link.substring(firstIndex + 7, link.length);
					if ('.' + id == selector) {
						isotopeFilter = '.' + id;
					}
				}
			});
			//$(window).load(function () {
				$container.isotope({
					//itemSelector: '.mb-productitem',
					filter: isotopeFilter
				});
			//});
			$optionLinks.each(function () {
				var $this = jQuery(this);
				var selector = $this.attr('data-filter');
				if (selector == isotopeFilter) {
					if (!$this.hasClass('mb-active')) {
						var $optionSet = $this.parents('.option-set');
						$optionSet.find('.mb-active').removeClass('mb-active');
						$this.addClass('mb-active');
					}
				}
			});
			$optionLinks.on('click', function () {
				var $this = jQuery(this);
				var selector = $this.attr('data-filter');
				$container.isotope({itemSelector: '.mb-project', filter: selector});
				if (!$this.hasClass('mb-active')) {
					var $optionSet = $this.parents('.option-set');
					$optionSet.find('.mb-active').removeClass('mb-active');
					$this.addClass('mb-active');
				}
				return false;
			});
		}
	}
	var isotopeTimer = window.setTimeout(function () {
		window.clearTimeout(isotopeTimer);
		doIsotopeFilter();
	}, 1000);

	/* DIRECTION AWARE HOVER*/
	jQuery(function () {
		jQuery('.wt-teamholder').each(function () {
			 jQuery(this).hoverdir();
		});
	});
	/* Brand Slider */
	var _wt_brandslider = jQuery("#wt-brandslider")
	_wt_brandslider.owlCarousel({
		item: 6,
		loop:false,
		nav:false,
		margin: 0,
		autoplay:false,
		responsiveClass:true,
		responsive:{
			0:{items:1,},
			481:{items:2,},
			768:{items:3,},
			991:{items:4,},
			992:{items:5,}
		}
	});
		$('#accordion').collapse({
	  toggle: false	
	})

	/* Team Slider */
	var _wt_categoriesslider = jQuery("#wt-categoriesslider")
	_wt_categoriesslider.owlCarousel({
		item: 6,
		loop:true,
		nav:false,
		margin: 0,
		autoplay:false,
		center: true,
		responsiveClass:true,
		responsive:{
			0:{items:1,},
			481:{items:2,},
			768:{items:3,},
			1440:{items:4,},
			1760:{items:6,}
		}
	});
	/* THEME VERTICAL SCROLLBAR */
	if(jQuery('.wt-verticalscrollbar').length > 0){
		var _wt_verticalscrollbar = jQuery('.wt-verticalscrollbar');
		_wt_verticalscrollbar.mCustomScrollbar({
			axis:"y",
		});
	}
	if(jQuery('.wt-horizontalthemescrollbar').length > 0){
		var _wt_horizontalthemescrollbar = jQuery('.wt-horizontalthemescrollbar');
		_wt_horizontalthemescrollbar.mCustomScrollbar({
			axis:"x",
			advanced:{autoExpandHorizontalScroll:true},
		});
	}
	/* TIPSO TOOLTIP */
	jQuery('.template-content').tipso({
			speed             : 400,        
			background        : '#fff',
			titleBackground   : '#3498db',
			color             : '#999999',
			titleColor        : '#ffffff',
			width             : 105,
			tooltipHover      : true,
			size :50,
			offsetY : 0,
			position: 'top-right'
		});

		jQuery('.hover-tipso-tooltip').tipso({
	    tooltipHover: true,
	});
	/* CONSULTATION FEE SLIDER */
	function ageRangeslider(){
		jQuery("#wt-productrangeslider").slider({
			range: true,
			min: 0,
			max: 150,
			values: [ 10, 110 ],
			slide: function( event, ui ) {
				jQuery( "#wt-consultationfeeamount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
			}
		});
		jQuery( "#wt-consultationfeeamount" ).val( "$" + jQuery("#wt-productrangeslider").slider( "values", 0 ) + " - $" + jQuery("#wt-productrangeslider").slider( "values", 1 ));
	}
	if( jQuery("#wt-productrangeslider").length > 0 ){
		ageRangeslider();
	}
	/* SHORT DESCRIPTION */
	var _readmore = jQuery('.wt-userdetails .wt-description');
	_readmore.readmore({
		speed: 500,
		collapsedHeight: 230,
		moreLink: '<a class="wt-btntext" href="#">Read More</a>',
		lessLink: '<a class="wt-btntext" href="#">Less</a>',
	});
	/*  PROGRESS BAR */
	try {
		$('#wt-ourskill').appear(function () {
			jQuery('.wt-skillholder').each(function () {
				jQuery(this).find('.wt-skillbar').animate({
					width: jQuery(this).attr('data-percent')
				}, 2500);
			});
		});
	} catch (err) {}
	/* PRELOADER*/
	jQuery(window).on('load', function() {
		jQuery(".preloader-outer").delay(1000).fadeOut();
		jQuery(".loader").delay(500).fadeOut("slow");
	});
	/*OPEN CLOSE */
	jQuery('.wt-projectdropdown').on('click', function(event){
		event.preventDefault();
		jQuery('.wt-projectdropdown-option').slideToggle();
	});
	/* DROPDOWN RADIO */
	jQuery('input:radio[name="searchtype"]').on('change',
	    function(){
	        var _type = jQuery(this).data('title');
	        jQuery('.selected-search-type').html(_type);
	    }
    );
    /* SIDEBAR DROPDOWN */
	jQuery('.wt-usersidebardown').on('click', function(event){
		event.preventDefault();
		jQuery('.wt-usersidebar').slideToggle();
	});

	/* Lost passowrd Box */
	jQuery('.wt-forgot-password').on('click', function (e) {     
		jQuery('.do-login-form').addClass('wt-hide-form');
		jQuery('.wt-loginheader span').html('Reset Password');
		jQuery('.do-forgot-password-form').removeClass('wt-hide-form');
	});
	jQuery('.wt-show-login').on('click', function (e) {       
		jQuery('.do-login-form').removeClass('wt-hide-form');
		jQuery('.wt-loginheader span').text('Login');
		jQuery('.do-forgot-password-form').addClass('wt-hide-form');
	});
	/* SEARCH CHOSEN */
	var config = {
		'.chosen-select'           : {},
		'.chosen-select-deselect'  : {allow_single_deselect:true},
		'.chosen-select-no-single' : {disable_search_threshold:10},
		'.chosen-select-no-results': {no_results_text:'Oops, nothing found!'},
		'.chosen-select-width'     : {width:"95%"}
		}
		for (var selector in config) {
			jQuery(selector).chosen(config[selector]);
	}
	
	/* CHATBOX TOGGLE  */
	jQuery('#wt-btnclosechat, #wt-getsupport').on('click', function(){
		jQuery('.wt-chatbox').slideToggle();
	});
	/* DASHBOARD MENU */
	if(jQuery('#wt-btnmenutoggle').length > 0){
		jQuery("#wt-btnmenutoggle").on('click', function(event) {
			event.preventDefault();
			jQuery('#wt-wrapper').toggleClass('wt-openmenu');
			jQuery('body').toggleClass('wt-noscroll');
			jQuery('.wt-navdashboard ul.sub-menu').hide();
		});
	}
	/* FIXED SIDEBAR */
	function fixedNav(){			
		$(window).scroll(function () {			
		var $pscroll = $(window).scrollTop();						
			if($pscroll > 76){
			 $('.wt-sidebarwrapper').addClass('wt-fixednav');
			}else{
			 $('.wt-sidebarwrapper').removeClass('wt-fixednav');
			}
		});
	}
	fixedNav();

	/* ADD Class */
	jQuery('.wt-myskills .wt-addinfo').on('click', function() {
		var _this = jQuery(this);
		_this.parents('li').addClass('wt-skillsaddinfo');
	});
	jQuery('.wt-myskills .wt-deleteinfo').on('click', function() {
		var _this = jQuery(this);
		var _val = _this.parents('li').find('.skill-dynamic-field input').val();
		_this.parents('li').find('.skill-dynamic-html .skill-val').html(_val);
		_this.parents('li').removeClass('wt-skillsaddinfo');
	});
	/* Dashboard Slider */
	var _wt_postedsilder = jQuery("#wt-postedsilder")
	_wt_postedsilder.owlCarousel({
		item: 6,
		loop:true,
		nav:true,
		margin: 10,
		autoplay:false,
		responsiveClass:true,
		navClass: ['wt-prev', 'wt-next'],
		navContainerClass: 'wt-slidernav',
		navText: ['<span class="lnr lnr-chevron-left"></span>', '<span class="lnr lnr-chevron-right"></span>'],
		responsive:{
			0:{items:1,},
			720:{items:2,},
		}
	});
	/* TINYMCE WYSIWYG EDITOR */
	if(jQuery('#wt-tinymceeditor').length > 0){
		tinymce.init({
			selector: 'textarea#wt-tinymceeditor',
			height: 300,
			theme: 'modern',
			plugins: [ 'advlist autolink lists link image charmap print preview hr anchor pagebreak'],
			menubar: false,
			statusbar: false,
			toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify',
			image_advtab: true,
		});
	}
	
	jQuery('.wt-savefollow').on('click', function(){
		event.preventDefault();
		$(this).parents('li').remove();
	});
	
	/* ADD AND REMOVE CLASS  */
	if(jQuery('.wt-ad').length > 0){
		var _wt_ad = jQuery('.wt-ad');
		_wt_ad.on('click',function () {
			jQuery(this).parents('.wt-messages-holder').addClass('wt-openmsg');
			jQuery(this).parent().parents('.wt-messages-holder').addClass('wt-openmsg');
		});
		var _wt_back = jQuery('.wt-back');
		_wt_back.on('click',function () {
			jQuery('.wt-back').parents('.wt-messages-holder').removeClass('wt-openmsg');
		});
	}
	
	/* JRATE STARS  */
	jQuery(function () {
		var that = this;
		var toolitup = $("#wt-jrate").jRate({
			rating: 5.0,
			strokeColor: '#dadadacc',
			precision: 1,
			startColor: "#fecb02",
			endColor: "#fecb02",
			backgroundColor: '#ddd',
			minSelected: 1,
			shapeGap: '10px',
			count: 5,
			onChange: function(rating) {
				jQuery('.counter').text(rating + '');
			},
			onSet: function(rating) {
				console.log("OnSet: Rating: "+rating);
			}
		});
	});
	
	jQuery(function () {
		var that = this;
		var toolitup = $("#wt-jrateone").jRate({
			rating: 4.0,
			strokeColor: '#dadadacc',
			precision: 1,
			startColor: "#fecb02",
			endColor: "#fecb02",
			backgroundColor: '#ddd',
			minSelected: 1,
			shapeGap: '10px',
			count: 5,
			onChange: function(rating) {
				jQuery('.counterone').text(rating + '');
			},
			onSet: function(rating) {
				console.log("OnSet: Rating: "+rating);
			}
		});
	});	
	
	jQuery(function () {
		var that = this;
		var toolitup = $("#wt-jratetwo").jRate({
			rating: 3.0,
			strokeColor: '#dadadacc',
			precision: 1,
			startColor: "#fecb02",
			endColor: "#fecb02",
			backgroundColor: '#ddd',
			minSelected: 1,
			shapeGap: '10px',
			count: 5,
			onChange: function(rating) {
				jQuery('.countertwo').text(rating + '');
			},
			onSet: function(rating) {
				console.log("OnSet: Rating: "+rating);
			}
		});
	});	
	
	jQuery(function () {
		var that = this;
		var toolitup = $("#wt-jratethree").jRate({
			rating: 2.0,
			strokeColor: '#dadadacc',
			precision: 1,
			startColor: "#fecb02",
			endColor: "#fecb02",
			backgroundColor: '#ddd',
			minSelected: 1,
			shapeGap: '10px',
			count: 5,
			onChange: function(rating) {
				jQuery('.counterthree').text(rating + '');
			},
			onSet: function(rating) {
				console.log("OnSet: Rating: "+rating);
			}
		});
	});	
	
});
	
