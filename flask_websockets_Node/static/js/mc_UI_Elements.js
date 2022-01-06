
//https://stackoverflow.com/questions/50508717/custom-elements-not-setting-getting-attributes



class mcRButton extends HTMLElement {


    constructor() {
    super();
    }

    connectedCallback() {
      let template = document.querySelector('#mcRB-template').content;
      this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
    
      let name_button = this.shadowRoot.querySelector("#name");
      let x_button = this.shadowRoot.querySelector("#x");
    
      name_button.textContent = this.getAttribute('name');
      name_button.style.background=this.getAttribute('color');//("background",);
      //console.log('create: '+ this.getAttribute('id'));

      name_button.addEventListener('click', () => {
        //console.log('select '+ this.shadowRoot.getAttribute('id'));
        socket.emit('ex', {msg: this.getAttribute('name'), id: this.getAttribute('id'), fn: "rem_butt_clicked"});
      });
    
      x_button.addEventListener('click', () => {

          console.log(name_button.parentElement);
          var parent = this.getRootNode().host;
          if (parent != null){ //is in shadowDom
            
            socket.emit('ex', {id: this.getAttribute('id'), parent: parent.getAttribute('id'), fn: "rem_butt_del_sbox"});
          }else
          {
            socket.emit('ex', {id: this.getAttribute('id'), parent: this.parentElement.getAttribute('id'), fn: "rem_butt_del"});
          }

      });

    }

}

customElements.define('mc-rbutton', mcRButton);



class mcRDropDown extends HTMLElement {

  constructor() {
  super();

    //set dropdown value: 
    //dropdown.value = opt[1];
  }

  connectedCallback() {
 
    let template = document.querySelector('#mcDD-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
  
    let dropdown = this.shadowRoot.querySelector("#dropdown");

    dropdown.addEventListener('change', () => {

      socket.emit('ex', {id: this.getAttribute('id'), opt: dropdown.options[dropdown.selectedIndex].text, fn: "sel"});
    });
  }


}

customElements.define('mc-dropdown', mcRDropDown);


class mcSlider extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
 
    let template = document.querySelector('#mcSlider-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
    let slider = this.shadowRoot.querySelector("#slider");
    let label = this.shadowRoot.querySelector("#label");
    label.innerHTML = this.getAttribute('id').toUpperCase();

    
    var isSlide = false;
    var lastval = 0;

    slider.addEventListener('mouseup', () => {
      //console.log(scrollbox.value);
      isSlide = false;
      //socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

    slider.addEventListener('mousedown', () => {
      isSlide = true;
    });
  
    slider.addEventListener('change', () => {
      //console.log(slider.value);
      socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

    slider.addEventListener('mousemove', (event, ui) => {
      if (isSlide){
        if (Math.abs(slider.value - lastval) > 2){
          console.log(slider.value);
          socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
          lastval = slider.value;
        }
      }

    });
  }
}

customElements.define('mc-slider', mcSlider);



class mcScrollBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcScrollBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    
    
    let scrollbox = this.shadowRoot.querySelector("#box");
    let label = this.shadowRoot.querySelector("#label");
    label.innerHTML = this.getAttribute('id').toUpperCase();

    var isScroll = false;

    scrollbox.addEventListener('mouseup', () => {
      //console.log(scrollbox.value);
      isScroll = false;
      //socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

    scrollbox.addEventListener('mousedown', () => {
      isScroll = true;
    });

    scrollbox.addEventListener('scroll', () => {
      var out = [$(scrollbox).scrollTop(), $(scrollbox).scrollLeft() ];
      if (isScroll){
          socket.emit('ex', {msg: out, id: this.getAttribute('id'), fn: "scb"});
          //console.log(out);
      }
    });
   
  }
}

customElements.define('mc-scrollbox', mcScrollBox);





class mcTextBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcTextBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let textbox = this.shadowRoot.querySelector("#text");
    let label = this.shadowRoot.querySelector("#label");
    label.innerHTML = this.getAttribute('id').toUpperCase();

    textbox.addEventListener('keyup', () => {
      console.log(textbox.value);
      socket.emit('ex', {id: this.getAttribute('id'), val: textbox.value, fn: "tex"});
    });

    textbox.addEventListener('change', () => {
      console.log(textbox.value);
      //socket.emit('ex', {id: this.getAttribute('id'), val: slider.value, fn: "sli"});
    });

   
  }
}

customElements.define('mc-textbox', mcTextBox);



class mcColorBox extends HTMLElement {

  constructor() {
  super();
  }

  connectedCallback() {
    let template = document.querySelector('#mcColorBox-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let colorbox = this.shadowRoot.querySelector("#color");

   
  }
}

customElements.define('mc-colorbox', mcColorBox);














function populateDropdown (id, data, active){
  for (let i = 0; i < data.length; i++) {
    document.getElementById(id).shadowRoot.getElementById("dropdown").append(new Option(data[i]));
  }
 document.getElementById(id).shadowRoot.getElementById("dropdown").value = active;
}











function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * 
            charactersLength));
        }
    return result;
}