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
		selector: '.explorer-posts-lightbox'
	});

	// initiate instagram stories lightbox
	const storiesLightbox = GLightbox({
		selector: '.stories-lightbox'
	});

	// scrolling buttons
	document.addEventListener("DOMContentLoaded", function() {
		const container = document.querySelector('.container');
		const scrollLeftButton = document.querySelector('.left-button');
		const scrollRightButton = document.querySelector('.right-button');
	
		// Function to check if container has overflow
		function checkOverflow() {
			return container.scrollWidth > container.clientWidth;
		}
	
		// Function to update button visibility
		function updateButtonVisibility() {
			scrollLeftButton.style.display = container.scrollLeft > 0 ? 'block' : 'none';
			scrollRightButton.style.display = container.scrollLeft < (container.scrollWidth - container.clientWidth) ? 'block' : 'none';
		}
	
		// Check overflow and update button visibility initially
		updateButtonVisibility();
	
		// Update button visibility on scroll
		container.addEventListener('scroll', updateButtonVisibility);
	
		// Scroll left and right button click handlers
		scrollLeftButton.addEventListener('click', function() {
			container.scrollLeft -= 100; // Adjust scroll amount as needed
			updateButtonVisibility();
		});
	
		scrollRightButton.addEventListener('click', function() {
			container.scrollLeft += 100; // Adjust scroll amount as needed
			updateButtonVisibility();
		});
	});
	
	
})();