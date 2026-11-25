<script setup lang="ts">
import { Axon } from "axon-gui";
import { ref } from "vue";

const out = ref("");

async function callPython() {
  // JS → Python：函数名就是 Python 里的方法名，参数直接摊开传。
  out.value = String(await Axon.Greeter.greet("Axon"));
}
</script>

<template>
  <main class="app">
    <img src="./assets/axon.svg" class="logo" alt="Axon" />
    <h1>Axon + Vue 3</h1>
    <p class="hint">点下面的按钮，会真的调用 Python 里的 Greeter.greet()。</p>
    <button type="button" class="btn" @click="callPython">调一次 Python</button>
    <pre class="out">{{ out || "还没有调用" }}</pre>
  </main>
</template>

<style scoped>
.app { max-width: 680px; margin: 0 auto; padding: 48px 24px; }
.logo { height: 88px; transition: filter 300ms; }
.logo:hover { filter: drop-shadow(0 0 1.6em #3451b2aa); }
h1 { font-size: 2rem; margin: 0.4em 0 0.2em; }
.hint { color: #9aa4b2; margin-bottom: 1.4em; }
.btn { font: inherit; padding: 8px 16px; cursor: pointer; }
.out { margin-top: 18px; padding: 12px 14px; background: #171a21; border-radius: 8px; min-height: 1.4em; text-align: left; }
</style>
