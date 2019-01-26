<template>
  <div class="d-flex align-items-stretch">
    <div class="mainPanel">
      <!--Stats cards-->
      <div class="row">
        <div class="col-md-6 col-xl-3" v-for="stats in statsCards" :key="stats.title">
          <stats-card>
            <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
              <i :class="stats.icon"></i>
            </div>
            <div class="numbers" slot="content">
              <p>{{stats.title}}</p>
              {{stats.value}}
            </div>
            <div class="stats" slot="footer">
              <i :class="stats.footerIcon"></i>
              {{stats.footerText}}
            </div>
          </stats-card>
        </div>
      </div>

      <!--Charts-->
      <div class="row">
        <div class="col-12">
          <chart-card
            title="System"
            sub-title="CPU and RAM statistics"
            :chart-data="systemChart.data"
            :chart-options="systemChart.options"
          >
            <span slot="footer">
              <i class="ti-reload"></i> Updated 3 minutes ago
            </span>
            <div slot="legend">
              <i class="fa fa-circle text-info"></i> CPU
              <i class="fa fa-circle text-warning"></i> RAM
            </div>
          </chart-card>
        </div>

        <div class="col-md-6 col-12">
          <chart-card
            title="Site Statistics"
            sub-title="Status of sites"
            :chart-data="siteChart.data"
            chart-type="Pie"
          >
            <span slot="footer">
              <i class="ti-reload"></i> Updated 3 minutes ago
            </span>
            <div slot="legend">
              <i class="fa fa-circle text-info"></i> Crawled
              <i class="fa fa-circle text-warning"></i> Pending
              <i class="fa fa-circle text-danger"></i> Syncing
            </div>
          </chart-card>
        </div>

        <div class="col-md-6 col-12">
          <card title="Control Panel">
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  ZeroNet
                  <button
                    class="btn btn-sm btn-outline-success ml-2"
                    v-if="!zeronetStatus"
                  >Start</button>
                  <button class="btn btn-sm btn-outline-warning ml-2" v-if="zeronetStatus">Stop</button>
                  <button class="btn btn-sm btn-outline-danger ml-2" v-if="zeronetStatus">Kill</button>
                </div>
                <div :class="{'text-success':zeronetStatus}">
                  {{upOrDown(zeronetStatus)}}
                  <i class="fa fa-power-off"></i>
                </div>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  HorizonSpider
                  <button
                    class="btn btn-sm btn-outline-success ml-2"
                    v-if="!spiderStatus"
                  >Start</button>
                  <button class="btn btn-sm btn-outline-warning ml-2" v-if="spiderStatus">Stop</button>
                  <button class="btn btn-sm btn-outline-danger ml-2" v-if="spiderStatus">Kill</button>
                </div>
                <div :class="{'text-success':spiderStatus}">
                  {{upOrDown(spiderStatus)}}
                  <i class="fa fa-power-off"></i>
                </div>
              </li>
            </ul>
            <div slot="footer">
              <i class="fa fa-terminal"></i>
              <span class="pl-2">{{status}}</span>
            </div>
          </card>
        </div>
      </div>
    </div>
    <div class="logsPanel flex-grow-1 ml-4" v-if>
      <card title="Log" subTitle="Logs of Spider and ZeroNet">
        <div class="card-body">
          <LogPage></LogPage>
        </div>
      </card>
    </div>
  </div>
</template>
<script>
import { StatsCard, ChartCard } from "@/components/index";
import Chartist from "chartist";
import LogPage from "./LogPage";
export default {
  components: {
    StatsCard,
    ChartCard,
    LogPage
  },
  methods: {
    restartSpider() {
      this.$socket.emit("restartSpider");
    },
    terminateSpider() {
      this.$socket.emit("terminateSpider");
    },
    fullRestart() {
      this.$socket.emit("fullRestart");
    },
    upOrDown(bool) {
      return bool ? "Up" : "Down";
    }
  },
  sockets: {
    connect() {
      console.log("Connected");
    },
    addLogs(arr) {
      console.log("Logs addded: " + arr.length);
    },
    setStatus(msg) {
      console.log("Status: " + msg);
      this.status = msg;
    }
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */
  data() {
    return {
      statsCards: [
        {
          type: "info",
          icon: "ti-server",
          title: "Used",
          value: "105GB",
          footerText: "Total 20GB",
          footerIcon: "ti-info-alt"
        },
        {
          type: "danger",
          icon: "ti-pulse",
          title: "Errors",
          value: "23",
          footerText: "In the last day",
          footerIcon: "ti-timer"
        },
        {
          type: "warning",
          icon: "ti-alert",
          title: "Warnings",
          value: "128",
          footerText: "In the last day",
          footerIcon: "ti-timer"
        },
        {
          type: "success",
          icon: "ti-world",
          title: "Sites",
          value: "4096",
          footerText: "Known sites",
          footerIcon: "ti-light-bulb"
        }
      ],
      systemChart: {
        data: {
          labels: [
            "9:00AM",
            "12:00AM",
            "3:00PM",
            "6:00PM",
            "9:00PM",
            "12:00PM",
            "3:00AM",
            "6:00AM"
          ],
          series: [
            [28, 38, 49, 56, 59, 62, 69, 89, 92],
            [23, 15, 19, 24, 38, 43, 53, 64, 74]
          ]
        },
        options: {
          low: 0,
          high: 100,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: false
        }
      },
      siteChart: {
        data: {
          labels: ["62%", "32%", "6%"],
          series: [62, 32, 6]
        },
        options: {}
      },
      status: "Unknown",
      zeronetStatus: false,
      spiderStatus: false
    };
  }
};
</script>
<style>
.mainPanel {
  max-width: 1000px;
}
.logsPanel .card {
  height: 100%;
}
@media screen and (max-width: 1800px) {
  .logsPanel {
    display: none;
  }
}
</style>
