<template>
    <BaseComponent>
        <MainContainer>
            <div class="full-width full-height" style="overflow: hidden; position: relative">
                <InputBar placeholder="Search..." button_text="Find" @search="search"/>
                <ItemsList>
                    <SearchItem v-for="video in videos" :title="video.title" :link="video.track_url.toString()"
                                :thumbnail="video.thumbnail_url.toString()" :duration="video.duration"/>

                </ItemsList>
                <div v-if="loading" class="spinner-overlay">
                    <div class="spinner"></div>
                </div>
            </div>
        </MainContainer>
    </BaseComponent>
</template>

<script>
import BaseComponent from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import InputBar from "@/components/elements/InputBar.vue";
import SearchItem from "@/components/search/SearchItem.vue";
import ItemsList from "@/components/containers/ItemsList.vue";
import {API_URL} from "@/services/consts";

export default {
    name: "Search",
    components: {ItemsList, SearchItem, InputBar, MainContainer, BaseComponent},
    data() {
        return {
            searchText: "",
            videos: [],
            loading: false,
        };
    },
    methods: {
        search(searchText) {
            this.loading = true;
            fetch(`${API_URL}/search?search_text=${searchText}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then(data => {
                    this.videos = data;
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                })
                .finally(() => {
                    this.loading = false;
                    this.$router.replace({ query: null });
                });
        }
    }
};

</script>


<style scoped>
.spinner {
    position: fixed;
    margin: 0 auto;
    width: 50px;
    height: 50px;
    border: 5px solid rgba(0, 0, 0, 0.1);
    border-left-color: #09f;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.spinner-overlay {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    background-color: rgba(0, 0, 0, 0.5);
}
</style>
