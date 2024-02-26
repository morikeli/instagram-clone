(function() {
	"use strict";

	// Easy selector helper function
	const select = (el, all = false) => {
		el = el.trim()
		if (all) {
			return [...document.querySelectorAll(el)]
		} else {
			return document.querySelector(el)
		}
	}

	// Easy event listener function
	const on = (type, el, listener, all = false) => {
		if (all) {
			select(el, all).forEach(e => e.addEventListener(type, listener))
		} else {
			select(el, all).addEventListener(type, listener)
		}
	}

	// Easy on scroll event listener 
	const onscroll = (el, listener) => {
		el.addEventListener('scroll', listener)
	}

	// side menu toggle
	if (select('.toggle-sidebar-btn')) {
		on('click', '.toggle-sidebar-btn', function(e) {
			select('#sidebar').classList.toggle('expand')
		})

		select('body').classList.add('toggle-sidebar');
	}

	function handleFormSubmission(event) {
		// Reset form fields
		document.getElementById('modal-form').reset();
		
		// Hide modal
		var modal = document.getElementById('comments-modal');
		modal.classList.remove('show');
		document.body.classList.remove('modal-open');
		var backdrop = document.getElementsByClassName('modal-backdrop')[0];
		if (backdrop) {
			backdrop.parentNode.removeChild(backdrop);
		}
	}
	
	// Add event listener to form after htmx:afterSwap event
	document.addEventListener('htmx:afterSwap', function(event) {
		if (event.target.id === 'comments-modal') {
			// Add event listener to the form after it's swapped
			document.getElementById('modal-form').addEventListener('htmx:response', handleFormSubmission);
		}
	});

	// initiate posts lightbox
	const postsLightbox = GLightbox({
		selector: '.expolorer-posts-lightbox'
	});

	document.addEventListener('DOMContentLoaded', function() {
		var carousel = document.getElementById('carouselExampleIndicators');
		var prevBtn = carousel.querySelector('.carousel-control-prev');
		var nextBtn = carousel.querySelector('.carousel-control-next');

		carousel.addEventListener('slid.bs.carousel', function() {
			var currentIndex = Array.from(carousel.querySelectorAll('.carousel-item')).indexOf(carousel.querySelector('.carousel-item.active'));
			prevBtn.style.display = currentIndex === 0 ? 'none' : 'block';
			nextBtn.style.display = currentIndex === carousel.querySelectorAll('.carousel-item').length - 1 ? 'none' : 'block';
		});
	});

})();