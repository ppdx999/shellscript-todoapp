// Base HTML elements generator
function el(tag, props = {}, children = []) {
	const element = document.createElement(tag);
	Object.entries(props).forEach(([key, value]) => {
		if (key.startsWith('on')) {
			// if the key starts with 'on', it's an event listener
			element.addEventListener(key.slice(2).toLowerCase(), value);
		} else if (typeof value === 'boolean') {
			element[key] = value;
		} else {
			element.setAttribute(key, value);
		}
	});
	children.forEach(child => {
		element.appendChild(typeof child === 'string' ? document.createTextNode(child) : child);
	});
	return element;
}

export function addStylesheet(href) {
	const link = document.createElement('link');
	link.rel = 'stylesheet';
	link.href = href;
	document.head.appendChild(link);
}

// HTML elements generator
export const h1 = (props, children) => el('h1', props, children);
export const div = (props, children) => el('div', props, children);
export const ul = (props, children) => el('ul', props, children);
export const li = (props, children) => el('li', props, children);
export const input = (props) => el('input', props);

