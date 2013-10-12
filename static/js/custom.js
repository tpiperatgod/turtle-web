//Opacity Focus Function
function item_opacity(){
	//Opacity Focus
	$("#mycarousel li, .portfolio li").hover(function() {
		$(this).siblings().stop().fadeTo(400,0.6);
	}, function() {
		$(this).siblings().stop().fadeTo(400,1);
	});
};
	

// In and Out effect for carousel
function item_hover(){
	$('ul#mycarousel li').hover(function(){		 
		$(this).children('.caption').animate({bottom:"0px"},{queue:false,duration:200});		 
		$(this).children('.lightbox').animate({top:"0px"},{queue:false,duration:200});
		$(this).children('.more').animate({top:"0px"},{queue:false,duration:200})	}, 
		function() {         
			$(this).children('.caption').animate({bottom:"-30px"},{queue:false,duration:200});		 
			$(this).children('.lightbox').animate({top:"-25px"},{queue:false,duration:200});	
			$(this).children('.more').animate({top:"-25px"},{queue:false,duration:200})
		});	
}


//gallery hover effect
function gallery_hover(){
	$('.gallery-item').hover(function(){		 
		$(this).children('a').animate({'opacity':0.5}, 200);
		$(this).children('.rollover').fadeIn(200); },	 
		function() {         
			$(this).children('a').animate({'opacity':1}, 200);
			$(this).children('.rollover').fadeOut(200);
		});	
}


//nivo-slider
$(window).load(function() {
	$('#slider').nivoSlider({
	    afterLoad: function(){
        var $slider = $('#slider');
        $slider.css('opacity',0);
        $('#preloader').fadeOut(500, function(){
           $slider.animate({'opacity':1}, 500);
        });
    }
	});
	
	item_hover();
	gallery_hover();
	item_opacity();
});



$(document).ready(function(){

//preload images
	$("#mycarousel, .post-thumbnail, #gallery").preloadify();

//subnav
	$('ul#mainnav').superfish({
		delay: 100,
		animation: {opacity:'show',opacity:'show'}, 
           speed: 'fast' 
	});
	$("ul#mainnav li").css({ "overflow":"visible"});

	$("ul#mainnav li ul li:last-child")
        .css({ "background":"url(images/subnav-bg.png) no-repeat scroll bottom center", "width":"200px", "height":"56px"});
	
	
//footer twitter function
	$(".tweet").tweet({
	  join_text: "auto",
	  username: "deliciousthemes",
	  count: 2,
	  template: "{join}{text}",
	  auto_join_text_reply: null,
      auto_join_text_default: null,        // [string]   auto text for non verb: "i said" bullocks
      auto_join_text_ed: null,                   // [string]   auto text for past tense: "i" surfed
      auto_join_text_ing: null,               // [string]   auto tense for present tense: "i was" surfing
      auto_join_text_reply: null,     // [string]   auto tense for replies: "i replied to" @someone "with"
      auto_join_text_url: null, 
	  loading_text: "loading tweets..."
	});	

	
//footer flickr function
	$('#flickr').jflickrfeed({
		limit: 15,
		qstrings: {
			id: '63991398@N07'
		},
		itemTemplate: 
		'<li>' +
			'<a href="{{image_b}}"><img src="{{image_s}}" alt="{{title}}" /></a>' +
		'</li>' 
	});	

	
//prettyphoto	
	$("a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'normal',theme:'light_square',slideshow:3000, autoplay_slideshow: false});

//z-index for header elements 
	var zIndexNumber = 1000;
		$('#top div').each(function() {
			$(this).css('zIndex', zIndexNumber);
			zIndexNumber -= 10;
		});	

		
// fade effect for blog post thumbnails		
	$('.post-thumbnail').hover(function(){		 
		$(this).children('a').animate({'opacity':0.8}, 300); }, 
		function() {         
			$(this).children('a').animate({'opacity':1}, 300);
		});	

		
//effect for scrolltop button		
	$('.totop').hover(function(){	
	$(this).animate({bottom:"-5px"},{queue:false,duration:200}); },
	function() {         
		$(this).animate({bottom:"-10px"},{queue:false,duration:200})
	});
	
	
//scroll to top
	$('.totop').click(function(){
            $("html, body").animate({ scrollTop: 0 }, 600);
            return false;
        });	


//carousel		
	$('#mycarousel').jcarousel();	


//portfolio slider
	$('#slides').slides({
		preload: true,
		preloadImage: 'images/nivo-preloader.gif',
		play: 5000,
		pause: 2500,
		fade: {
		 interval: 1000, // [Number] Interval of fade in milliseconds
		 crossfade: true, // [Boolean] TODO: add this feature. Crossfade the slides, great for images, bad for text
		 easing: "" // [String] Dependency: jQuery Easing plug-in <http://gsgd.co.uk/sandbox/jquery/easing/>
		},
		effects: {
		 navigation: "fade",  // [String] Can be either "slide" or "fade"
		 pagination: "fade" // [String] Can be either "slide" or "fade"
		},
		hoverPause: true
	});

	
//social icons fading effect
	$("#social li").hover(function() {
		$(this).children('a').animate({opacity:"1"},{queue:false,duration:300}) },
		function() {
			$(this).children('a').animate({opacity:"0.5"},{queue:false,duration:300})
			});


//accordion	function		
	$('.ac-btn').click(function() {
		$('.ac-btn').removeClass('on');
	 	$('.ac-content').slideUp('normal');
		if($(this).next().is(':hidden') == true) {
			$(this).addClass('on');
			$(this).next().slideDown('normal');
		 }   
	 });
	$('.ac-btn').mouseover(function() {
		$(this).addClass('over');
	}).mouseout(function() {
		$(this).removeClass('over');										
	});	
	$('.ac-content').hide();


//tabs function
	$('.tabs-wrapper').each(function() {
		$(this).find(".tab-content").hide(); //Hide all content
		$(this).find("ul.tabs li:first").addClass("active").show(); //Activate first tab
		$(this).find(".tab-content:first").show(); //Show first tab content
	});
	$("ul.tabs li").click(function(e) {
		$(this).parents('.tabs-wrapper').find("ul.tabs li").removeClass("active"); //Remove any "active" class
		$(this).addClass("active"); //Add "active" class to selected tab
		$(this).parents('.tabs-wrapper').find(".tab-content").hide(); //Hide all tab content

		var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
		$("li.tab-item:first-child").css("background", "none" );
		$(this).parents('.tabs-wrapper').find(activeTab).fadeIn(); //Fade in the active ID content
		e.preventDefault();
	});
	$("ul.tabs li a").click(function(e) {
		e.preventDefault();
	})
	$("li.tab-item:last-child").addClass('last-item');
	

// toggle function
$('#toggle-view li').click(function () {
        var text = $(this).children('div.panel');
        if (text.is(':hidden')) {
            text.slideDown('200');
            $(this).children('span').addClass('toggle-minus');     
        } else {
            text.slideUp('200');
			$(this).children('span').removeClass('toggle-minus'); 
            $(this).children('span').addClass('toggle-plus');     
        }
         
    });


//gallery masonry
  $(function(){
    var $container = $('#gallery'); 
    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.gallery-item'
      });
    });
  });

});
  
// Portfolio Sorting
	(function($) {
	
		
		$.fn.sorted = function(customOptions) {
			var options = {
				reversed: false,
				by: function(a) {
					return a.text();
				}
			};
	
			$.extend(options, customOptions);
	
			$data = jQuery(this);
			arr = $data.get();
			arr.sort(function(a, b) {
	
				var valA = options.by($(a));
				var valB = options.by($(b));
		
				if (options.reversed) {
					return (valA < valB) ? 1 : (valA > valB) ? -1 : 0;				
				} else {		
					return (valA < valB) ? -1 : (valA > valB) ? 1 : 0;	
				}
		
			});
	
			return $(arr);
	
		};
	
	})(jQuery);
	
	jQuery(function() {
	
		var read_button = function(class_names) {
			
			var r = {
				selected: false,
				type: 0
			};
			
			for (var i=0; i < class_names.length; i++) {
				
				if (class_names[i].indexOf('selected') == 0) {
					r.selected = true;
				}

			};
			
			return r;
			
		};
	
		var determine_sort = function($buttons) {
			var $selected = $buttons.parent().filter('[class*="selected"]');
			return $selected.find('a').attr('data-value');
		};
	
		var determine_kind = function($buttons) {
			var $selected = $buttons.parent().filter('[class*="selected"]');
			return $selected.find('a').attr('data-value');
		};
	
		var $preferences = {
			duration: 500,
			adjustHeight: 'dynamic'
		}
	
		var $list = jQuery('.portfolio');
		var $data = $list.clone();
	
		var $controls = jQuery('#filters');
		
		$(".portfolio").preloadify();
	
		$controls.each(function(i) {
	
			var $control = jQuery(this);
			var $buttons = $control.find('a');
	
			$buttons.bind('click', function(e) {
	
				var $button = jQuery(this);
				var $button_container = $button.parent();
				
				var button_properties = read_button($button_container.attr('class').split(' '));      
				var selected = button_properties.selected;
				var button_segment = button_properties.segment;
	
				if (!selected) {
	
					$buttons.parent().removeClass();
					$button_container.addClass('selected');
	
					var sorting_type = determine_sort($controls.eq(1).find('a'));
					var sorting_kind = determine_kind($controls.eq(0).find('a'));
	
					if (sorting_kind == 'all') {
						var $filtered_data = $data.find('li');
					} else {
						var $filtered_data = $data.find('li.' + sorting_kind);
					}
	
					var $sorted_data = $filtered_data.sorted({
						by: function(v) {
							return parseInt(jQuery(v).find('.count').text());
						}
					});
	
					$list.quicksand($sorted_data, $preferences, function () {
						item_opacity();
						item_hover();
						
						
					});
					
					//console.log($sorted_data);
		
				}
		
				e.preventDefault();
				
			});
		
		}); 
		
	});
