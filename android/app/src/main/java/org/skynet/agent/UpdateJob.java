package org.skynet.agent;

import android.app.job.JobInfo;
import android.app.job.JobParameters;
import android.app.job.JobScheduler;
import android.app.job.JobService;
import android.content.ComponentName;
import android.content.Context;
import android.os.Handler;
import android.os.Looper;

import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class UpdateJob extends JobService {
    private static final int ID = 200;
    private JobParameters active;
    private Future<?> task;

    static void schedule(Context ctx) {
        JobScheduler jobs = ctx.getSystemService(JobScheduler.class);
        if (jobs.getPendingJob(ID) == null) {
            jobs.schedule(new JobInfo.Builder(ID, new ComponentName(ctx, UpdateJob.class))
                    .setRequiredNetworkType(JobInfo.NETWORK_TYPE_ANY)
                    .setPeriodic(TimeUnit.DAYS.toMillis(1)).setPersisted(true).build());
        }
    }

    @Override
    public boolean onStartJob(JobParameters params) {
        active = params;
        task = ApkUpdates.worker.submit(() -> {
            ApkUpdates.check(getApplicationContext());
            new Handler(Looper.getMainLooper()).post(() -> {
                if (active == params) {
                    active = null;
                    jobFinished(params, false);
                }
            });
        });
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) {
        active = null;
        task.cancel(true);
        return true;
    }
}
