class TrashIcon extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Shadow DOM内にSVGを埋め込み、デフォルトのサイズを設定
    shadow.innerHTML = `
      <style>
        svg {
          width: 16px;  /* デフォルトのサイズ */
          height: 16px; /* デフォルトのサイズ */
          fill: currentColor;
          cursor: pointer;
        }
      </style>
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
				<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
				<path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
			</svg>
    `;
  }

  connectedCallback() {
    const svg = this.shadowRoot.querySelector('svg');
    const width = this.getAttribute('width') || '16px';
    const height = this.getAttribute('height') || '16px';

    svg.style.width = width;
    svg.style.height = height;
  }

  static get observedAttributes() {
    return ['width', 'height'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    const svg = this.shadowRoot.querySelector('svg');
    if (name === 'width') svg.style.width = newValue;
    if (name === 'height') svg.style.height = newValue;
  }
}

customElements.define('trash-icon', TrashIcon);
