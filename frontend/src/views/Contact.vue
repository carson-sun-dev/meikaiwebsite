<template>
  <div class="contact-page">
    <div class="contact-page__navbg" aria-hidden="true">
      <NavigationBar />
    </div>

    <main class="contact-page__main">
      <HomeSectionFade>
        <ContactQuoteForm @submit="onContactSubmit" />
      </HomeSectionFade>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'
import HomeSectionFade from '@/components/home/HomeSectionFade.vue'
import ContactQuoteForm from '@/components/contact/ContactQuoteForm.vue'

function onContactSubmit(payload: unknown) {
  // TODO: 这里后续接入后端：保存用户姓氏/称呼 + 联系方式 + 用户选择的估价选项
  console.log('[contact] submit payload:', payload)
}
</script>

<style scoped>
.contact-page {
  min-height: 100dvh;
  background: #fff;
  color: #000;
}

.contact-page__navbg {
  background: #000;
  padding: 0;
}

.contact-page__main {
  padding: 3rem 0 2.5rem;
}

@media (max-width: 768px) {
  .contact-page__main {
    padding-top: 2.25rem;
  }
}
</style>

