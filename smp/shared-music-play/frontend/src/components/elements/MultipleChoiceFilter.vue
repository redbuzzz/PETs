<template>
  <div class="filter">
    <div class="filter-header" v-if="this.title">{{ this.title }}</div>
  <div v-for="option in this.options">
      <input type="checkbox"
             :value="option.value"
             :id="idPrefix + option.value"
             :checked="isChecked(option)"
             @change="toggleOption(option)"
             class="filter-checkbox"
      />
      <label :for="idPrefix + option.value" class="filter-checkbox-label">
        {{ option.name || option.value }}
      </label>
    </div>
  </div>
</template>

<script>
import _ from "lodash";

export default {
  name: "MultipleChoiceFilter",
  props: {
    options: {
      type: Array,
      required: true
    },
    activeOptions: {
      type: Array,
      required: true
    },
    allowMany: {
      type: Boolean,
      default: true
    },
    allowNoSelection: {
      type: Boolean,
      default: true
    },
    idPrefix: {
      type: String,
      default: "filter-"
    },
    title: {
      type: String,
      default: ""
    }
  },
  methods: {
    isChecked(option) {
      return _.some(this.activeOptions, _.matches(option));
    },
    toggleOption(option) {
      // awful logic here, no KISS

      let updatedActiveOptions;

      if (!this.allowMany) {
        // only 1 or 0 can be selected
        updatedActiveOptions = [option];

        if (this.allowNoSelection && this.isChecked(option)) {
          updatedActiveOptions = [];
        }

      } else if (!this.allowNoSelection) { // allow many and must select one

        if (this.isChecked(option)) {
          updatedActiveOptions = this.activeOptions.filter((o) => !_.isEqual(o, option) );
          if (updatedActiveOptions.length === 0) {
            updatedActiveOptions = [option]
          }
        }

      } else if (this.isChecked(option)) {
        updatedActiveOptions = this.activeOptions.filter((o) => !_.isEqual(o, option));
      } else {
        updatedActiveOptions = this.activeOptions.concat(option);
      }

      this.$emit("updateActiveOptions", updatedActiveOptions);
    },
  }
}
</script>

<style scoped>
.filter {
    margin-bottom: 10px;
    display: flex;
    flex-direction: row;
}

.filter-header {
    font-weight: 500;
    font-size: 32px;
    color: #FFFFFF;
    margin-right: 7px;
}

.filter-checkbox-label {
    width: 164px;
    height: 40px;
    margin-left: 30px;
    background: #D9D9D9;
    display: flex;
    align-items: center;
    justify-content: center;
}

.filter-checkbox {
    display: none;
}

.filter-checkbox:checked + .filter-checkbox-label {
    opacity: .8;
}

</style>
