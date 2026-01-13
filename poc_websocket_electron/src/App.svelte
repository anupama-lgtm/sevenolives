<script>
  import Window1 from './components/Window1.svelte';
  import Window2 from './components/Window2.svelte';

  // Get the hash from URL to determine which window to show
  let currentRoute = window.location.hash.replace('#', '') || '/window1';

  // Listen for hash changes
  window.addEventListener('hashchange', () => {
    currentRoute = window.location.hash.replace('#', '') || '/window1';
  });
</script>

<main>
  {#if currentRoute === '/window1'}
    <Window1 />
  {:else if currentRoute === '/window2'}
    <Window2 />
  {:else}
    <Window1 />
  {/if}
</main>

<style>
  main {
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }
</style>
