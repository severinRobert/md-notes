<template>
  <textarea
    :value="text"
    @change="$emit('update:text', text)"
    cols="30"
    rows="10"
    @keydown.ctrl.1.prevent="title($event, 1)"
    @keydown.ctrl.2.prevent="title($event, 2)"
    @keydown.ctrl.3.prevent="title($event, 3)"
    @keydown.ctrl.4.prevent="title($event, 4)"
    @keydown.ctrl.b.prevent="bold"
    @keydown.ctrl.i.prevent="italic"
  />
</template>

<script>
export default {
  name: 'MarkdowEditor',
  props: {
    text: {
      type: String,
      required: true
    }
  },
  emits: ['update:text'],
  methods: {
    insert(text, symbole, index) {
      console.log(text, symbole, index)
      return text.slice(0, index) + symbole + text.slice(index)
    },
    surround(text, symbole, start, end) {
      const before = text.slice(0, start)
      const between = text.slice(start, end)
      const after = text.slice(end)
      return before + symbole + between + symbole + after
    },
    removeSurroundSymbole(text, symbole, start, end) {
      const before = text.lastIndexOf(symbole, start)
      const after = text.indexOf(symbole, end) + symbole.length
      return (
        text.slice(0, before) +
        text.slice(before, after).replaceAll(symbole, '') +
        text.slice(after)
      )
    },
    isSurrounded(text, symbole) {
      if (
        text.slice(0, symbole.length) == symbole &&
        text.slice(text.length - symbole.length) == symbole
      ) {
        return true
      }
      return false
    },
    title(e, number) {
      console.log('title ', number)
      const startOfTheLine = this.text.lastIndexOf('\n', e.target.selectionStart) + 1
      console.log(startOfTheLine)
      this.$emit("update:text", this.insert(this.text, '#'.repeat(number) + ' ', startOfTheLine))
    },
    bold(e) {
      const selectionStart = e.target.selectionStart
      const selectionEnd = e.target.selectionEnd
      if (this.isSurrounded(this.text.slice(selectionStart, selectionEnd), '__')) {
        this.$emit("update:text", this.removeSymbole(this.text, '__', selectionStart, selectionEnd))
      } else {
        this.$emit("update:text", this.surround(this.text, '__', selectionStart, selectionEnd))
      }
      console.log(document.getElementsByTagName('textarea')[0].value)
      document.getElementsByTagName('textarea')[0].setSelectionRange(selectionStart, selectionEnd)
    },
    italic(e) {
      const selectionStart = e.target.selectionStart
      const selectionEnd = e.target.selectionEnd
      if (this.isSurrounded(this.text.slice(selectionStart, selectionEnd), '_')) {
        this.$emit("update:text", this.removeSymbole(this.text, '_', selectionStart, selectionEnd))
      } else {
        this.$emit("update:text", this.surround(this.text, '_', selectionStart, selectionEnd))
      }
    }
  }
}
</script>

<style scoped>
textarea {
  box-sizing: border-box;
  width: 100%;
  height: 99%;
  border: none;
  resize: none;
}
</style>
