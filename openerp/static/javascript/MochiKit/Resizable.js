MochiKit.DragAndDrop.Resizables = {
    /***

    Manage Resizables elements. Not intended to direct use.

    ***/
    resizers: [],

    observers: [],

    register: function (resizable) {
        if (this.resizers.length === 0) {
            var bind = MochiKit.Base.bind;
            var conn = MochiKit.Signal.connect;
            
            this.eventMouseUp = conn(document, 'onmouseup', this, 'endResize'); 
            this.eventMouseMove = conn(document, 'onmousemove', this, 'updateResize'); 
            this.eventKeypress = conn(document, 'onkeypress', this, 'keyPress');
        }
        this.resizers.push(resizable);
    },

    unregister: function (resizable) {
        this.resizers = MochiKit.Base.filter(function (d) {
            return d != resizable;
        }, this.resizers);
        if (this.resizers.length === 0) {
            var disc = MochiKit.Signal.disconnect
            disc(this.eventMouseUp); 
            disc(this.eventMouseMove); 
            disc(this.eventKeypress);
        }
    },

    activate: function (resizable) {
        // allows keypress events if window is not currently focused
        // fails for Safari
        window.focus();
        this.activeResizable = resizable;
    },

    deactivate: function () {
        this.activeResizable = null;
    },

    updateResize: function (event) {
        if (!this.activeResizable) {
            return;
        }
        var pointer = event.mouse();
        // Mozilla-based browsers fire successive mousemove events with
        // the same coordinates, prevent needless redrawing (moz bug?)
        if (this._lastPointer && (MochiKit.Base.repr(this._lastPointer.page) ==
                                  MochiKit.Base.repr(pointer.page))) {
            return;
        }
        this._lastPointer = pointer;
        this.activeResizable.updateResize(event, pointer);
    },

    endResize: function (event) {
        if (!this.activeResizable) {
            return;
        }
        this._lastPointer = null;
        this.activeResizable.endResize(event);
        this.activeResizable = null;
    },

    keyPress: function (event) {
        if (this.activeResizable) {
            this.activeResizable.keyPress(event);
        }
    },
    
    notify: function (eventName, draggable, event) {    
        MochiKit.Signal.signal(this, eventName, draggable, event);
    }
};

MochiKit.DragAndDrop.Resizable = function (element, options) {
    this.__init__(element, options);
};

MochiKit.DragAndDrop.Resizable.prototype = {
    /***

    A resizable object. Simple instantiate :

        new MochiKit.DragAndDrop.Resizable('myelement');

    ***/
    __class__ : MochiKit.DragAndDrop.Resizable,

    __init__: function (element, /* optional */options) {
        var v = MochiKit.Visual;
        options = MochiKit.Base.update({
            handle: false,
            starteffect: function (element) {
                new v.Opacity(element, {duration:0.2, from:1.0, to:0.7});
            },
            reverteffect: function (element, top_offset, left_offset) {
                var dur = Math.sqrt(Math.abs(top_offset^2) +
                          Math.abs(left_offset^2))*0.02;
                element._revert = new v.Move(element,
                            {x: -left_offset, y: -top_offset, duration: dur});
            },
            endeffect: function (element) {
                new v.Opacity(element, {duration:0.2, from:0.7, to:1.0});
            },
            zindex: 1000,
            revert: false,
            scroll: false,
            scrollSensitivity: 20,
            scrollSpeed: 15,
            // false, or xy or [x, y] or function (x, y){return [x, y];}
            snap: false,
            min: [0, 0],
            max: false
        }, options || {});

        var d = MochiKit.DOM;
        this.element = d.getElement(element);

        if (options.handle && (typeof(options.handle) == 'string')) {
            this.handle = d.getFirstElementByTagAndClassName(null,
                                       options.handle, this.element);
        }
        if (!this.handle) {
            this.handle = d.getElement(options.handle);
        }
        if (!this.handle) {
            this.handle = this.element;
        }

        if (options.scroll && !options.scroll.scrollTo && !options.scroll.outerHTML) {
            options.scroll = d.getElement(options.scroll);
        }

        d.makePositioned(this.element);  // fix IE
        
        this.options = options;
        this.delta = this.currentDelta();
        this.resizing = false;

        this.eventMouseDown = MochiKit.Signal.connect(this.handle, 'onmousedown', this, 'initResize');
        MochiKit.DragAndDrop.Resizables.register(this);
    },

    destroy: function () {
        MochiKit.Signal.disconnect(this.eventMouseDown);
        MochiKit.DragAndDrop.Resizables.unregister(this);
    },

    currentDelta: function () {
        var s = MochiKit.DOM.getStyle;
        return [
          parseInt(s(this.element, 'left') || '0'),
          parseInt(s(this.element, 'top') || '0')];
    },

    initResize: function (event) {
        if (!event.mouse().button.left) {
            return;
        }
        // abort on form elements, fixes a Firefox issue
        var src = event.target;
        if (src.tagName && (
            src.tagName == 'INPUT' ||
            src.tagName == 'SELECT' ||
            src.tagName == 'OPTION' ||
            src.tagName == 'BUTTON' ||
            src.tagName == 'TEXTAREA')) {
            return;
        }

        if (this.element._revert) {
            this.element._revert.cancel();
            this.element._revert = null;
        }

        var pointer = event.mouse();
        var pos = MochiKit.Position.cumulativeOffset(this.element);
        this.offset = [pointer.page.x - pos[0], pointer.page.y - pos[1]]
                
        var dim = MochiKit.DOM.elementDimensions(this.element);
        
        this.dimensions = [0, 0];
        this.borders = [0, 0];
                        
        this.dimensions[0] = parseInt(MochiKit.DOM.getStyle(this.element, 'width')) || 0;
        this.dimensions[1] = parseInt(MochiKit.DOM.getStyle(this.element, 'height')) || 0;
        
        this.borders[0] = dim.w - this.dimensions[0];
        this.borders[1] = dim.h - this.dimensions[1];
        
        MochiKit.DragAndDrop.Resizables.activate(this);
        event.stop();
    },

    startResize: function (event) {
        this.resizing = true;
        if (this.options.selectclass) {
            MochiKit.DOM.addElementClass(this.element,
                                         this.options.selectclass);
        }
        if (this.options.onselect) {
            this.options.onselect(this.element);
        }
        if (this.options.zindex) {
            this.originalZ = parseInt(MochiKit.DOM.getStyle(this.element,
                                      'z-index') || '0');
            this.element.style.zIndex = this.options.zindex;
        }

        if (this.options.ghosting) {
            this._clone = this.element.cloneNode(true);
            MochiKit.Position.absolutize(this.element);
            this.element.parentNode.insertBefore(this._clone, this.element);
        }

        if (this.options.scroll) {
            if (this.options.scroll == window) {
                var where = this._getWindowScroll(this.options.scroll);
                this.originalScrollLeft = where.left;
                this.originalScrollTop = where.top;
            } else {
                this.originalScrollLeft = this.options.scroll.scrollLeft;
                this.originalScrollTop = this.options.scroll.scrollTop;
            }
        }

        MochiKit.DragAndDrop.Resizables.notify('onStart', this, event);
        if (this.options.starteffect) {
            this.options.starteffect(this.element);
        }
    },

    updateResize: function (event, pointer) {
        if (!this.resizing) {
            this.startResize(event);
        }
        MochiKit.Position.prepare();
        MochiKit.DragAndDrop.Resizables.notify('onResize', this, event);
        this.draw(pointer);
        if (this.options.change) {
            this.options.change(this);
        }

        if (this.options.scroll) {
            this.stopScrolling();
            var p;
             if (this.options.scroll == window) {
                var s = this._getWindowScroll(this.options.scroll);
                p = [s.left, s.top, s.left+s.width, s.top+s.height];
            } else {
                p = MochiKit.Position.page(this.options.scroll);
                p[0] += this.options.scroll.scrollLeft;
                p[1] += this.options.scroll.scrollTop;
                p.push(p[0] + this.options.scroll.offsetWidth);
                p.push(p[1] + this.options.scroll.offsetHeight);
            }
            var speed = [0, 0];
            if (pointer.page.x < (p[0] + this.options.scrollSensitivity)) {
                speed[0] = pointer.page.x - (p[0] + this.options.scrollSensitivity);
            }
            if (pointer.page.y < (p[1] + this.options.scrollSensitivity)) {
                speed[1] = pointer.page.y - (p[1] + this.options.scrollSensitivity);
            }
            if (pointer.page.x > (p[2] - this.options.scrollSensitivity)) {
                speed[0] = pointer.page.x - (p[2]-this.options.scrollSensitivity);
            }
            if (pointer.page.y > (p[3] - this.options.scrollSensitivity)) {
                speed[1] = pointer.page.y - (p[3] - this.options.scrollSensitivity);
            }
            this.startScrolling(speed);
        }

        // fix AppleWebKit rendering
        if (MochiKit.Base.isSafari()) {
            window.scrollBy(0, 0);
        }
        event.stop();
    },

    finishResize: function (event, success) {
        var dr = MochiKit.DragAndDrop;
        this.resizing = false;
        if (this.options.selectclass) {
            MochiKit.DOM.removeElementClass(this.element,
                                            this.options.selectclass);
        }
        if (this.options.ondeselect) {
            this.options.ondeselect(this.element);
        }

        if (this.options.ghosting) {
            // XXX: from a user point of view, it would be better to remove
            // the node only *after* the MochiKit.Visual.Move end
            MochiKit.Position.relativize(this.element);
            MochiKit.DOM.removeElement(this._clone);
            this._clone = null;
        }

        dr.Resizables.notify('onEnd', this, event);

        var revert = this.options.revert;
        if (revert && typeof(revert) == 'function') {
            revert = revert(this.element);
        }

        var d = this.currentDelta();
        if (revert && this.options.reverteffect) {
            this.options.reverteffect(this.element,
                d[1] - this.delta[1], d[0] - this.delta[0]);
        } else {
            this.delta = d;
        }

        if (this.options.zindex) {
            this.element.style.zIndex = this.originalZ;
        }

        if (this.options.endeffect) {
            this.options.endeffect(this.element);
        }

        dr.Resizables.deactivate();
    },

    keyPress: function (event) {
        if (event.keyString != "KEY_ESCAPE") {
            return;
        }
        this.finishResize(event, false);
        event.stop();
    },

    endResize: function (event) {
        if (!this.resizing) {
            return;
        }
        this.stopScrolling();
        this.finishResize(event, true);
        event.stop();
    },

    draw: function (point) {
        var pos = MochiKit.Position.cumulativeOffset(this.element);
        var d = this.currentDelta();
        pos[0] -= d[0];
        pos[1] -= d[1];

        if (this.options.scroll && !this.options.scroll.scrollTo) {
            pos[0] -= this.options.scroll.scrollLeft - this.originalScrollLeft;
            pos[1] -= this.options.scroll.scrollTop - this.originalScrollTop;
        }

        var p = [point.page.x - pos[0] - this.offset[0],
                 point.page.y - pos[1] - this.offset[1]];

        p[0] += this.dimensions[0];
        p[1] += this.dimensions[1];           
        
        if (this.options.snap) {
            if (typeof(this.options.snap) == 'function') {
                p = this.options.snap(p[0], p[1]);
            } else {
                if (this.options.snap instanceof Array) {
                    var i = -1;
                    p = MochiKit.Base.map(MochiKit.Base.bind(function (v) {
                            i += 1;
                            return Math.round(v/this.options.snap[i]) *
                                   this.options.snap[i]
                        }, this), p)
                } else {
                    p = MochiKit.Base.map(MochiKit.Base.bind(function (v) {
                        return Math.round(v/this.options.snap) *
                               this.options.snap
                        }, this), p)
                }
            }
        }                     
        
        p[0] -= d[0] + this.borders[0];
        p[1] -= d[1] + this.borders[1];                      
                
        if (this.options.min) {
            p[0] = p[0] > this.options.min[0] ? p[0] : this.options.min[0];
            p[1] = p[1] > this.options.min[1] ? p[1] : this.options.min[1];
        }
        
        if (this.options.max) {
            p[0] = p[0] < this.options.max[0] ? p[0] : this.options.max[0];
            p[1] = p[1] < this.options.max[1] ? p[1] : this.options.max[1];
        }
        
        var style = this.element.style;
        if ((!this.options.constraint) ||
            (this.options.constraint == 'horizontal')) {                        
            style.width = p[0] + 'px';
        }
        if ((!this.options.constraint) ||
            (this.options.constraint == 'vertical')) {
            style.height = p[1] + 'px';
        }
        if (style.visibility == 'hidden') {
            style.visibility = '';  // fix gecko rendering
        }
    },

    stopScrolling: function () {
        if (this.scrollInterval) {
            clearInterval(this.scrollInterval);
            this.scrollInterval = null;
        }
    },

    startScrolling: function (speed) {
        this.scrollSpeed = [speed[0] * this.options.scrollSpeed, speed[1] * this.options.scrollSpeed];
        this.lastScrolled = new Date();
        this.scrollInterval = setInterval(MochiKit.Base.bind(this.scroll, this), 10);
    },

    scroll: function () {
        var current = new Date();
        var delta = current - this.lastScrolled;
        this.lastScrolled = current;
        
        if (this.options.scroll == window) {
            var s = this._getWindowScroll(this.options.scroll);
            if (this.scrollSpeed[0] || this.scrollSpeed[1]) {
                var d = delta / 1000;
                this.options.scroll.scrollTo(s.left + d*this.scrollSpeed[0], s.top + d*this.scrollSpeed[1]);
            }
        } else {
            this.options.scroll.scrollLeft += this.scrollSpeed[0] * delta / 1000;
            this.options.scroll.scrollTop += this.scrollSpeed[1] * delta / 1000;
        }
        
        var d = MochiKit.DragAndDrop;
        
        MochiKit.Position.prepare();
        this.draw(d.Resizables._lastPointer);
        if (this.options.change) {
            this.options.change(this);
        }
    },

    _getWindowScroll: function (w) {
        var T, L, W, H;
        with (w.document) {
            if (w.document.documentElement && documentElement.scrollTop) {
                T = documentElement.scrollTop;
                L = documentElement.scrollLeft;
            } else if (w.document.body) {
                T = body.scrollTop;
                L = body.scrollLeft;
            }
            if (w.innerWidth) {
                W = w.innerWidth;
                H = w.innerHeight;
            } else if (w.document.documentElement && documentElement.clientWidth) {
                W = documentElement.clientWidth;
                H = documentElement.clientHeight;
            } else {
                W = body.offsetWidth;
                H = body.offsetHeight
            }
        }
        return {top: T, left: L, width: W, height: H};
    },

    repr: function () {
        return '[' + this.__class__.NAME + ", options:" + MochiKit.Base.repr(this.options) + "]";
    }
};