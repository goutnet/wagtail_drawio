/**
 * Drawio widget
 * Simple widget to embed drawio editor in a page.
 *
 * Copyright (C) 2023 - Florian Delizy
 *
 * This code is distributed under the MIT License.
 * https://opensource.org/licenses/MIT
 */

/**
 * DrawioEditor:
 * A class to manage the drawio editor.
 *
 * Usage:
 * 1. Include the drawio_widget.js in your page.
 * 2. Define the DRAWIO_EDITOR_URL in your page js.
 * 3. Add the class 'drawio-widget' to the image element.
 * 4. define the id for your image element.
 *
 * then either:
 *
 * 5. Add the event listener to the image element:
 *   document.addEventListener('DOMContentLoaded', function() {
 *   new DrawioEditor('id-to-your-drawio-widget');
 *
 * OR:
 *
 * 5. use jQuery to initialize the widget:
 *  jQuery(document).ready(function() {
 *    jQuery('.drawio-widget').drawio();
 *    });
 *
 * OR (automatically with jQuery):
 *
 * 5. add the data-drawio-widget attribute to the image element:
 *  <img id="my-drawio-widget" class="drawio-widget" data-drawio-widget />
 *
 *
 * Configuration of the widget is done via the following data attributes:
 *
 * data-drawio-widget: the image element is a drawio widget (optional)
 *
 * data-event: the event to trigger the editor (default: dblclick)
 * data-storage: the id of the element to store the image data (default: none)
 * data-xml: the id of the element to store the xml data (default: none)
 * data-width: the id of the element to store the width (default: none)
 * data-height: the id of the element to store the height (default: none)
 *
 * data-update-size: update the size of the image element (default: false)
 */


class DrawioEditor
{
    constructor(elementId, eventName=null)
    {
        this.element = document.getElementById(elementId); // the image element

        if (this.element == null) {
            console.error("Drawio: Element not found:", elementId);
            return;
        }


        this.drawio = null; // will hold the contentWindow of the iframe
        this.iframe = null; // the iframe element

        if (eventName == null) {
            const name = this._getFlag('event');
            if (name) {
                eventName = name;
            } else {
                eventName = 'dlbclick';
            }
        }
        this._eventName = eventName;

        // Set up event handlers
        this.element.addEventListener(this._eventName, () => this.activate());
    }

    _getTarget(suffix)
    {
        // Check data-target to find target element
        const targetId = this.element.getAttribute('data-' + suffix);
        console.log('drawio: target"' + suffix +'" is:', targetId);

        if (targetId == null) {
            return null;
        }

        if (targetId == '@self') {
            return this.element;
        }

        if (targetId[0] == '#') {
            return document.getElementById(targetId.slice(1));
        }

        if (targetId[0] == '.') {
            const lst = document.getElementsByClassName(targetId.slice(1));
            if (lst.length > 0) {
                return lst[0];
            }
        }

        console.warning("drawio: invalid target:", targetId);
        return null;
    }

    _getFlag(suffix)
    {
        // Check data-flag to find target element
        const flag = this.element.getAttribute('data-' + suffix);
        return flag;
    }

    activate()
    {
        const url = DRAWIO_EDITOR_URL;

        const iframe = document.createElement('iframe');
        iframe.setAttribute('frameborder', '0');
        iframe.setAttribute('class', 'drawio-editor');

        iframe.close = () => {
            window.removeEventListener('message', this.receive);
            document.body.removeChild(iframe);
            this.drawio = null;
            this.iframe = null;
        };

        if (this.drawio == null || this.drawio.closed) {

            window.addEventListener('message', (evt) => this.receive(evt));

            iframe.setAttribute('src', url);
            document.body.appendChild(iframe);
            this.drawio = iframe.contentWindow;
            this.iframe = iframe;

        } else {
            this.drawio.focus();
        }
    }


    // Protocol implementation:
    _onInit(msg)
    {
        this.drawio.postMessage(JSON.stringify({
            action: 'load', xmlpng: this.element.getAttribute('src')
        }), '*');
    }

    _onSave(msg)
    {
        this.drawio.postMessage(JSON.stringify({
            action: 'export', format: 'xmlpng', spinKey: 'saving'
        }), '*');
    }


    _onExit(msg)
    {
        this.iframe.close();
    }

    _onExport(msg)
    {
        this.element.setAttribute('src', msg.data);

        const storage = this._getTarget('storage');
        if (storage) {
            storage.value = msg.data;
        }

        const xml = this._getTarget('xml');
        if (xml) {
            xml.value = msg.xml;
        }

        // Round the size:
        const width = Math.round(msg.bounds.width);
        const height = Math.round(msg.bounds.height);

        const dwidth = this._getTarget('width');
        if (dwidth) {
            dwidth.value = width;
        }

        const dheight = this._getTarget('height');
        if (dheight) {
            dheight.value = height;
        }

        if (this._getFlag('update-size')) {
            this.element.style.width = width + 'px';
            this.element.style.height = height + 'px';
        }
        // Auto exit:
        this._onExit(msg);
    }

    _states = {
        'init': this._onInit,
        'save': this._onSave,
        'export': this._onExport,
        'exit': this._onExit
    };

    // protocol router
    // doc https://www.drawio.com/doc/faq/embed-mode
    receive(evt)
    {
        if (evt.data.length > 0 && evt.source == this.drawio) {
            const msg = JSON.parse(evt.data);
            if (msg.event in this._states) {
                this._states[msg.event].call(this, msg);
            } else {
                console.log('DrawIO: Unknown message:', msg);
            }

        }
    }

}

if (jQuery && jQuery.fn && typeof(jQuery.fn.drawio) == 'undefined') {
    jQuery.fn.drawio = function() {
        this.each(function() {
           this.drawio = new DrawioEditor(this.id);
        });
    }

    // Automatially initialize the widgets:
    jQuery(document).ready(function() {
        jQuery('.drawio-widget[data-drawio-widget]').drawio();
    });
}
