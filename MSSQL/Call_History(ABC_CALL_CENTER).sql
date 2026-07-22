use ABC_Call_Centre;
--drop table call_history;


USE ABC_Call_Centre;
GO

IF OBJECT_ID('dbo.call_history','U') IS NOT NULL
BEGIN
    DROP TABLE dbo.call_history;
END
GO

CREATE TABLE dbo.call_history
(
    id INT IDENTITY(1,1) PRIMARY KEY,

    call_id NVARCHAR(100) NOT NULL UNIQUE,

    agent_id NVARCHAR(100) NULL,

    call_date DATE NULL,

    call_start TIME(2) NULL,

    call_end TIME(2) NULL,

    call_duration TIME(0) NULL,

    duration_seconds INT NULL,

    created_at DATETIME NOT NULL DEFAULT(GETDATE()),

    updated_at DATETIME NULL
);
GO



INSERT INTO dbo.call_history
(
    call_id,
    agent_id,
    call_date,
    call_start,
    call_end,
    call_duration,
    duration_seconds,
    created_at
)

SELECT

    W.[Call ID],

    MAX(W.agent_id),

    ---------------------------------------------------
    -- Call Date
    ---------------------------------------------------
    CAST
    (
        MIN
        (
            CASE
                WHEN W.event_name='CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        ) AS DATE
    ),

    ---------------------------------------------------
    -- Call Start
    ---------------------------------------------------
    CAST
    (
        MIN
        (
            CASE
                WHEN W.event_name='CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        ) AS TIME(2)
    ),

    ---------------------------------------------------
    -- Call End
    ---------------------------------------------------
    CAST
    (
        MAX
        (
            CASE
                WHEN W.event_name='CallHandler.CallEnded'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        ) AS TIME(2)
    ),

    ---------------------------------------------------
    -- Duration
    ---------------------------------------------------
    CAST
    (
        DATEADD
        (
            SECOND,

            DATEDIFF
            (
                SECOND,

                MIN
                (
                    CASE
                        WHEN W.event_name='CallHandler.CallStarted'
                        THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
                    END
                ),

                MAX
                (
                    CASE
                        WHEN W.event_name='CallHandler.CallEnded'
                        THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
                    END
                )
            ),

            '00:00:00'
        )

        AS TIME(0)

    ),

    ---------------------------------------------------
    -- Duration Seconds
    ---------------------------------------------------
    DATEDIFF
    (
        SECOND,

        MIN
        (
            CASE
                WHEN W.event_name='CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        ),

        MAX
        (
            CASE
                WHEN W.event_name='CallHandler.CallEnded'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        )

    ),

    GETDATE()

FROM webhook_events W

GROUP BY
    W.[Call ID]

ORDER BY
    MIN
    (
        CASE
            WHEN W.event_name='CallHandler.CallStarted'
            THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
        END
    );







select * from call_history;

select * from webhook_events;
DELETE FROM dbo.webhook_events
WHERE [Call ID] = 'Mahin'; 
select * from updated_sheet1;




--delete table 
USE ABC_Call_Centre;
GO

IF OBJECT_ID('dbo.call_history', 'U') IS NOT NULL
    DROP TABLE dbo.call_history;
GO


--view create 
USE ABC_Call_Centre;
GO

IF OBJECT_ID('dbo.call_history', 'V') IS NOT NULL
    DROP VIEW dbo.call_history;
GO

CREATE VIEW dbo.call_history
AS

SELECT

    W.[Call ID] AS call_id,

    MAX(W.agent_id) AS agent_id,

    CAST
    (
        MIN
        (
            CASE
                WHEN W.event_name = 'CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2, W.webhook_delivered_at)
            END
        ) AS DATE
    ) AS call_date,

    CAST
    (
        MIN
        (
            CASE
                WHEN W.event_name = 'CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2, W.webhook_delivered_at)
            END
        ) AS TIME(2)
    ) AS call_start,

    CAST
    (
        MAX
        (
            CASE
                WHEN W.event_name = 'CallHandler.CallEnded'
                THEN TRY_CONVERT(datetime2, W.webhook_delivered_at)
            END
        ) AS TIME(2)
    ) AS call_end,

    CAST
    (
        DATEADD
        (
            SECOND,

            DATEDIFF
            (
                SECOND,

                MIN
                (
                    CASE
                        WHEN W.event_name='CallHandler.CallStarted'
                        THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
                    END
                ),

                MAX
                (
                    CASE
                        WHEN W.event_name='CallHandler.CallEnded'
                        THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
                    END
                )
            ),

            '00:00:00'
        )

        AS TIME(0)

    ) AS call_duration,

    DATEDIFF
    (
        SECOND,

        MIN
        (
            CASE
                WHEN W.event_name='CallHandler.CallStarted'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        ),

        MAX
        (
            CASE
                WHEN W.event_name='CallHandler.CallEnded'
                THEN TRY_CONVERT(datetime2,W.webhook_delivered_at)
            END
        )

    ) AS duration_seconds

FROM webhook_events W

GROUP BY
    W.[Call ID];
GO



--for seeing call_histoy
use ABC_Call_Centre;
SELECT *
FROM call_history
ORDER BY call_date, call_start;




select * from webhook_events;
select * from updated_sheet1;







--DROP VIEW dbo.call_history;
--Drop table dbo.call_history;
--DROP table call_history,complain_call_master,corporate_office,error_log,pca_data,updated_sheet1,verbex_fashions,verbex_garments,verbex_washing,webhook_events;
--select * from webhook_events;