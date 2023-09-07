<template>
  <section id="edit-view">
    <section id="file-tree"></section>
    <section id="edit">
      <MarkdownEditor v-model:text="text" />
    </section>
    <MarkdownRenderer id="render" :source="text" />
  </section>
</template>

<script>
import MarkdownEditor from '../components/MarkdownEditor.vue';
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'

export default {
  name: 'HomeView',
  components: {
    MarkdownEditor,
    MarkdownRenderer,
  },
  data() {
    return {
      text: 'lorem ipsum est un le',
    }
  },
  methods: {
  },
}
</script>

<style scoped>

#edit-view {
  display: flex;
  flex-direction: row;

  height: 100vh;
  width: 100vw;
}

#file-tree, #edit, #render {
  margin: var(--margin);
  border: 1px black solid;
}

#file-tree {
  width: calc(20vw - 2*var(--margin));
}

#edit {
  width: calc(40vw - 2*var(--margin));
}

#render {
  width: calc(40vw - 2*var(--margin));
  padding: 0.5rem;
}
</style>
