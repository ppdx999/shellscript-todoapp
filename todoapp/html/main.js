import { div, ul, li, input } from './core/view.js';

function transition(state, action) {
	switch (action.type) {
		case 'TOGGLE_TODO':
			return {
				...state,
				todos: state.todos.map(todo => {
					if (todo.id === action.id) {
						return { ...todo, completed: !todo.completed };
					}
					return todo;
				}),
			};
		default:
			return state;
	}
}

let state = {
	todos: [],
};

function dispatch(action) {
	state = transition(state, action);
	render()
}

function todoItem(todo) {
	return li({}, [
		input({
			name: 'todoitem',
			type: 'checkbox',
			checked: todo.completed,
			onchange: () => dispatch({ type: 'TOGGLE_TODO', id: todo.id })
		}),
		todo.title
	]);
}

function todolist(state) {
	return ul({}, state.todos.map(todoItem));
}

function ui(state) {
	return div({}, [
		div({}, ["Todo App"]),
		todolist(state)
	]);
}

function render() {
	document.body.innerHTML = '';
	document.body.appendChild(ui(state));
}

async function fetchState() {
	// TODO: Fetch state from the server
	return {
		todos: [
			{ id: 1, title: "Learn JavaScript", completed: true },
			{ id: 2, title: "Learn React", completed: false },
			{ id: 3, title: "Build something awesome", completed: false },
		],
	};
}

async function init() {
	// TODO: Fetch initial state from the server
	state = await fetchState();
	render();
}

document.addEventListener('DOMContentLoaded', init);
