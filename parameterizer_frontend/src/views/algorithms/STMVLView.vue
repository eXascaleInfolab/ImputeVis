<template>
  <h3 class="mb-4 text-center">ST-MVL Detail</h3>
  <div v-if="loadingResults" class="d-flex justify-content-center mt-3">
    <div class="alert alert-info d-flex align-items-center">
      <div class="spinner-border text-primary me-3" role="status"></div>
      Determining resulting imputation...
    </div>
  </div>
  <div class="d-flex mb-auto">
    <div class="col-lg-10">
      <highcharts v-if="imputedData" :options="chartOptionsImputed"></highcharts>
      <highcharts v-if="!imputedData" :options="chartOptionsOriginal"></highcharts>
    </div>
    <div class="col-lg-2">
      <form @submit.prevent="submitForm" class="sidebar me-3">
        <data-select v-model="dataSelect" @update:seriesNames="updateSeriesNames"/>
        <normalization-toggle v-model="normalizationMode"></normalization-toggle>
        <missing-rate v-model="missingRate"/>
        <!--Window Size-->
        <div class="mb-3">
          <label for="windowSize" class="form-label">Window Size: {{ windowSize }}</label>
          <input id="windowSize" v-model.number="windowSize" type="range" min="2" max="100" step="1"
                 class="form-control">
        </div>

        <!--Smoothing Parameter Gamma-->
        <div class="mb-3">
          <label for="gamma" class="form-label">Smoothing Parameter (γ): {{ gamma }}</label>
          <input id="gamma" v-model.number="gamma" type="range" min="0.05" max="0.99" step="0.05" class="form-control">
        </div>

        <!-- Power for Spatial Weight (Alpha) -->
        <div class="mb-3">
          <label for="alpha" class="form-label">Power for Spatial Weight (α): {{ alpha }}</label>
          <input id="alpha" v-model.number="alpha" type="range" min="0.5" max="20" step="0.5" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary">Impute</button>
        <div class="mt-3">
          <metrics-display v-if="imputedData" :metrics="metrics"></metrics-display>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import {ref, watch, computed} from 'vue';
import DataSelect from '../components/DataSelect.vue';
import MetricsDisplay from '../components/MetricsDisplay.vue';
import MissingRate from '../components/MissingRate.vue';
import NormalizationToggle from '../components/NormalizationToggle.vue'
import axios from 'axios';
import {Chart} from 'highcharts-vue'
import Highcharts from 'highcharts'
import HighchartsBoost from 'highcharts/modules/boost'
import {
  createSegmentedSeries,
  createSeries,
  generateChartOptions,
  generateChartOptionsLarge
} from "@/views/thesisUtils/utils";

// HighchartsBoost(Highcharts)

export default {
  components: {
    DataSelect,
    highcharts: Chart,
    MetricsDisplay,
    MissingRate,
    NormalizationToggle,
  },
  setup() {
    const dataSelect = ref('climate_eighth') // Default data
    const normalizationMode = ref('Normal')
    let currentSeriesNames = []; // Names of series currently displayed
    const missingRate = ref('10'); // Default missing rate
    const windowSize = ref('2'); // Default window size is 2
    const gamma = ref('0.5') // Default smoothing parameter gamma is 0.5, min 0.0, max 1.0
    const alpha = ref('2') // Default power for spatial weight (alpha) is 2, must be larger than 0.0
    const imputedData = ref(false); // Whether imputation has been carried out
    const rmse = ref(null);
    const mae = ref(null);
    const mi = ref(null);
    const corr = ref(null);

    let obfuscatedMatrix = [];
    let groundtruthMatrix = [];
    let loadingResults = ref(false);
    const metrics = computed(() => ({rmse: rmse.value, mae: mae.value, mi: mi.value, corr: corr.value}));

    const fetchData = async () => {
      try {
        imputedData.value = false;
        let dataSet = `${dataSelect.value}_obfuscated_${missingRate.value}`;
        const response = await axios.post('http://localhost:8000/api/fetchData/',
            {
              data_set: dataSet,
              normalization: normalizationMode.value,
            },
            {
              headers: {
                'Content-Type': 'application/json',
              }
            }
        );
        chartOptionsOriginal.value.series.splice(0, chartOptionsOriginal.value.series.length);

        obfuscatedMatrix = response.data.matrix;
        groundtruthMatrix = response.data.groundtruth;
        response.data.matrix.forEach((data: number[], index: number) => {
          // Replace NaN with 0
          const cleanData = data.map(value => isNaN(value) ? 0 : value);
          if (currentSeriesNames.length > 0) {
            chartOptionsOriginal.value.series[index] = createSeries(index, cleanData, dataSelect.value, currentSeriesNames[index]);
          } else {
            chartOptionsOriginal.value.series[index] = createSeries(index, cleanData, dataSelect.value);
          }
        });
      } catch (error) {
        console.error(error);
      }
    }

    const submitForm = async () => {
      try {
        let dataSet = `${dataSelect.value}_obfuscated_${missingRate.value}`;
        loadingResults.value = true;
        imputedData.value = false;
        const response = await axios.post('http://localhost:8000/api/stmvl/',
            {
              data_set: dataSet,
              normalization: normalizationMode.value,
              window_size: windowSize.value,
              gamma: gamma.value,
              alpha: alpha.value,
            },
            {
              headers: {
                'Content-Type': 'application/json',
              }
            }
        );
        rmse.value = response.data.rmse.toFixed(3);
        mae.value = response.data.mae.toFixed(3);
        mi.value = response.data.mi.toFixed(3);
        corr.value = response.data.corr.toFixed(3);
        chartOptionsImputed.value.series.length = 0;
        // Create a new array for the new series data
        const newSeriesData = [];

        const displayImputation = missingRate.value != '60' && missingRate.value != '80'
        response.data.matrix_imputed.forEach((data: number[], index: number) => {
          if (currentSeriesNames.length > 0 && missingRate) {
            if (displayImputation) {
              newSeriesData.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], groundtruthMatrix[index], chartOptionsImputed.value, dataSelect.value, currentSeriesNames[index]));
            } else {
              newSeriesData.push(createSeries(index, data, dataSelect.value, currentSeriesNames[index]));
            }
          } else {
            if (displayImputation) {
              newSeriesData.push(...createSegmentedSeries(index, data, obfuscatedMatrix[index], groundtruthMatrix[index], chartOptionsImputed.value, dataSelect.value));
            } else {
              newSeriesData.push(createSeries(index, data, dataSelect.value))
            }
          }
        });
        // Directly modify the existing object without deep cloning
        chartOptionsImputed.value.series = newSeriesData;
        imputedData.value = true;
      } catch (error) {
        console.error(error);
      } finally {
        loadingResults.value = false;
      }
    }
    const chartOptionsOriginal = ref(generateChartOptions('Original Data', 'Data'));
    const chartOptionsImputed = ref(generateChartOptionsLarge('Imputed Data', 'Data'));

    // Define a new function that calls fetchData
    const handleDataSelectChange = () => {
      chartOptionsImputed.value = generateChartOptionsLarge('Imputed Data', 'Data')
      fetchData();
    }

    const updateSeriesNames = (newSeriesNames) => {
      currentSeriesNames = newSeriesNames;
    };

    const handleNormalizationModeChange = () => {
      if (imputedData.value == true) {
          fetchData();
          submitForm();
      } else {
          handleDataSelectChange();
      }
    }

    // Watch for changes and call fetchData when it changes
    watch([dataSelect, missingRate], handleDataSelectChange, {immediate: true});
    watch(normalizationMode, handleNormalizationModeChange, {immediate: true});

    return {
      submitForm,
      metrics,
      chartOptionsOriginal,
      chartOptionsImputed,
      updateSeriesNames,
      dataSelect,
      normalizationMode,
      windowSize,
      gamma,
      alpha,
      missingRate,
      imputedData,
      loadingResults
    }
  }
}
</script>

<style scoped>
.sidebar {
  margin-left: 35px; /* Change this value to increase or decrease the margin */
}
</style>