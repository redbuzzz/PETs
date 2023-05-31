<template>
  <div id="nav-bar">
    <div class="nav-top-buttons">
      <RouterLink to="/profile">
        <ProfileSVG/>
      </RouterLink>
      <RouterLink to="/">
        <HomeSVG/>
      </RouterLink>
    </div>
    <div class="nav-bottom-buttons">
      <RouterLink to="/logout">
        <LogoutSVG/>
      </RouterLink>
    </div>
  </div>
</template>

<script>
import ProfileSVG from "@/components/svgs/ProfileSVG.vue";
import LogoutSVG from "@/components/svgs/LogoutSVG.vue";
import HomeSVG from "@/components/svgs/HomeSVG.vue";

export default {
  name: "NavBar",
  components: {HomeSVG, LogoutSVG, ProfileSVG}
}

</script>

<style scoped>
#nav-bar {
  width: 70px;
  height: 100%;
  background-color: #1F1F1F;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: width 1s ease-in-out;
}

.nav-top-buttons, .nav-bottom-buttons {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
