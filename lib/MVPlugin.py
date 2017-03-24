import json
import os.path as path
import os
import codecs
filename = "MechaWrap"
mechaWrapCommand = "<wrap>"
mechaWrapBreak = "<br>"
pluginPush = """$plugins.push({"name":"MechaWrap","status":true,"description":"v1.0.0 This plugin provides word wrap feature, so that a long text will be properly broken down into lines.","parameters":{}})"""

def addPlugin (mainFile):
    mainFolder = path.abspath(path.dirname(mainFile))
    jsFolder = path.join(mainFolder, path.join("www", "js"))
    pluginsJS = path.join(jsFolder, "plugins.js")
    pluginsFolder = path.join(jsFolder, "plugins")
    wrapJS = path.join(pluginsFolder, filename + ".js")

    try:
        with codecs.open(pluginsJS, "r", encoding="utf-8") as f:
            plugins = f.read().splitlines()
            f.close()
        if pluginPush not in plugins:
            plugins.append(pluginPush)
            with codecs.open(pluginsJS, "w", encoding="utf-8") as f:
                f.write("\r\n".join(plugins))
                f.close()
            if not path.exists(pluginsFolder):
                os.makedirs(pluginsFolder)
            with codecs.open(wrapJS, "w", encoding="utf-8") as f:
                f.write("\r\n".join(mechaWrapPluginJs.splitlines()))
                f.close()
    except Exception as e:
        print("Unable to add Word Wrap plugin: " + str(e))


mechaWrapPluginJs = """/*:
 * Yami Engine Delta - Word Wrap
 *
 * @plugindesc v1.0.0 This plugin provides word wrap feature, so that a long text will be properly broken down into lines.
 * @author Yami Engine Delta [Dr.Yami]
 *
 * @help
 * The word wrap isn't enabled by default. To activate word wrap in any text,
 * for example in Message, you have to put following code into the text:
 *
 *   <wrap>
 *
 * To make a long word to be broken, you can add the following code into the text:
 *
 *   <breakword>
 *
 * The word wrapper will nullify the break lines in editor, so that you have
 * to manually break line by using following code in text:
 *
 *   <br>
 *
 * ============================================================================
 */

(function() {
    var _Window_Base_processNormalCharacter
        = Window_Base.prototype.processNormalCharacter
    var _Window_Base_convertEscapeCharacters
        = Window_Base.prototype.convertEscapeCharacters

    Window_Base.prototype.textAreaWidth = function() {
        return this.contentsWidth()
    }

    Window_Base.prototype.needWrap = function(textState) {
        var c = textState.text[textState.index],
            w = this.textWidth(c),
            nextSpaceIndex = 0,
            nextBreakIndex = 0,
            nextWord = "",
            nextWidth = 0,
            text = textState.text,
            breakWord = !!this._breakWord

        if (!this._yamiWordWrap) {
            return false
        }

        if (breakWord && (textState.x + w * 2) >= this.textAreaWidth()) {
            textState.index-- // hack for missing character
            return true
        }

        if (!breakWord && c === " ") {
            nextSpaceIndex = text.indexOf(" ", textState.index + 1)
            nextBreakIndex = text.indexOf("\\n", textState.index + 1)

            if (nextSpaceIndex < 0) {
                nextSpaceIndex = text.length + 1
            }

            if (nextBreakIndex > 0) {
                nextSpaceIndex = Math.min(nextSpaceIndex, nextBreakIndex)
            }

            nextWord = text.substring(textState.index, nextSpaceIndex)

            nextWidth = this.textWidth(nextWord)

            if (textState.x + nextWidth >= this.textAreaWidth()) {
                return true
            }
        }

        return false
    }

    Window_Base.prototype.convertEscapeCharacters = function(text) {
        text = _Window_Base_convertEscapeCharacters.call(this, text)
        text = this.convertWordWrapEscapeCharacters(text)

        return text
    }

    Window_Base.prototype.convertWordWrapEscapeCharacters = function(text) {
        text = this.enableWordWrap(text)

        if (!!this._yamiWordWrap) {
            text = text.replace(/[\\n\\r]+/g, '')
            text = text.replace(/<br>/gi, '\\n')
        }

        return text
    }

    Window_Base.prototype.enableWordWrap = function(text) {
        this._yamiWordWrap = false
        this._breakWord = false

        if (!!text.match(/<wrap>/i)) {
            this._yamiWordWrap = true
        }

        if (!!text.match(/<breakword>/i)) {
            this._breakWord = true
        }

        text = text.replace(/<wrap>/gi, '')
        text = text.replace(/<breakword>/gi, '')

        return text
    }

    Window_Base.prototype.processNormalCharacter = function(textState) {
        if (this.needWrap(textState)) {
            return this.processNewLine(textState)
        }

        _Window_Base_processNormalCharacter.call(this, textState)
    }
}())"""