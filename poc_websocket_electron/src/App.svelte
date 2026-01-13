<script>
  import Window1 from './components/Window1.svelte';
  import Window2 from './components/Window2.svelte';
</script>

<main class="page">
  <header class="topbar">Django Sync POC - Svelte Frontend</header>
  <section class="columns">
    <div class="column">
      <Window1 />
    </div>
    <div class="column">
      <Window2 />
    </div>
  </section>
</main>

<style>
  .page {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  .topbar {
    color: #fff;
    font-weight: 700;
    padding: 16px 24px;
    font-size: 18px;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    padding: 24px;
    overflow: auto;
  }
  .column { min-width: 0; }
</style>
